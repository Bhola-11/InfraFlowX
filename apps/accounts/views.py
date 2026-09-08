from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q

from .models import User, UserProfile, UserLoginSession, USER_ROLE_CHOICES
from .forms import (
    EnterpriseAuthenticationForm, 
    EnterpriseUserRegistrationForm, 
    UserProfileUpdateForm, 
    UserPreferencesForm,
    AdminUserCreateForm,
    AdminUserUpdateForm
)
from apps.organizations.models import Organization
from apps.permissions.decorators import role_required, permission_required
from apps.audit.utils import log_audit_event

def login_view(request):
    """
    Enterprise authentication view with session logging and audit recording.
    """
    if request.user.is_authenticated:
        return redirect('analytics:dashboard')

    if request.method == 'POST':
        form = EnterpriseAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Record user activity
            user.last_activity = timezone.now()
            user.save(update_fields=['last_activity'])
            
            # Record Login Session
            UserLoginSession.objects.create(
                user=user,
                ip_address=getattr(request, 'client_ip', None),
                user_agent=getattr(request, 'user_agent_str', '')[:255],
                session_key=request.session.session_key or ''
            )

            # Audit Log
            log_audit_event(
                action='LOGIN',
                module='accounts',
                object_id=user.pk,
                object_repr=user.username,
                description=f"User {user.username} logged into system from IP {getattr(request, 'client_ip', 'unknown')}",
                request=request
            )

            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            next_url = request.GET.get('next') or 'analytics:dashboard'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please verify your credentials.")
    else:
        form = EnterpriseAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    Enterprise logout with session teardown and audit logging.
    """
    if request.user.is_authenticated:
        user = request.user
        log_audit_event(
            action='LOGOUT',
            module='accounts',
            object_id=user.pk,
            object_repr=user.username,
            description=f"User {user.username} logged out.",
            request=request
        )
        logout(request)
        messages.info(request, "You have been securely logged out.")
    return redirect('accounts:login')


def register_view(request):
    """
    Self-service enterprise user registration.
    """
    if request.user.is_authenticated:
        return redirect('analytics:dashboard')

    if request.method == 'POST':
        form = EnterpriseUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            log_audit_event(
                action='CREATE',
                module='accounts',
                object_id=user.pk,
                object_repr=user.username,
                description=f"User {user.username} registered with role {user.get_role_display()}",
                request=request
            )
            login(request, user)
            messages.success(request, f"Registration complete. Welcome to InfraFlowX, {user.first_name}!")
            return redirect('analytics:dashboard')
    else:
        form = EnterpriseUserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request, pk=None):
    """
    User profile summary displaying roles, organization, assigned equipment, recent audit actions.
    """
    if pk:
        user = get_object_or_404(User, pk=pk)
    else:
        user = request.user

    profile, _ = UserProfile.objects.get_or_create(user=user)
    recent_sessions = user.login_sessions.all()[:10]
    recent_audit_logs = user.audit_logs.all()[:10]

    context = {
        'profile_user': user,
        'profile': profile,
        'recent_sessions': recent_sessions,
        'recent_audit_logs': recent_audit_logs,
        'is_own_profile': user == request.user,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_settings_view(request):
    """
    User settings view: edit personal info, avatar, UI theme, notification preferences.
    """
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserProfileUpdateForm(request.POST, request.FILES, instance=user)
        pref_form = UserPreferencesForm(request.POST, instance=profile)

        if user_form.is_valid() and pref_form.is_valid():
            user_form.save()
            pref_form.save()
            log_audit_event(
                action='UPDATE',
                module='accounts',
                object_id=user.pk,
                object_repr=user.username,
                description="User updated profile details and preferences.",
                request=request
            )
            messages.success(request, "Your profile and preferences have been updated successfully.")
            return redirect('accounts:profile')
    else:
        user_form = UserProfileUpdateForm(instance=user)
        pref_form = UserPreferencesForm(instance=profile)

    context = {
        'user_form': user_form,
        'pref_form': pref_form,
    }
    return render(request, 'accounts/settings.html', context)


@login_required
def password_change_view(request):
    """
    Security password change view.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            log_audit_event(
                action='UPDATE',
                module='accounts',
                object_id=user.pk,
                object_repr=user.username,
                description="User successfully changed their security password.",
                request=request
            )
            messages.success(request, "Your password has been changed successfully.")
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/password_change.html', {'form': form})


# Admin User Management Views
@login_required
@role_required(['super_admin', 'organization_admin'])
def user_list_view(request):
    """
    Enterprise user directory with role, organization, and status filters.
    """
    query = request.GET.get('q', '').strip()
    role_filter = request.GET.get('role', '')
    org_filter = request.GET.get('org', '')
    status_filter = request.GET.get('status', '')

    users_qs = User.objects.select_related('organization').all()

    if query:
        users_qs = users_qs.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(badge_number__icontains=query)
        )
    if role_filter:
        users_qs = users_qs.filter(role=role_filter)
    if org_filter:
        users_qs = users_qs.filter(organization_id=org_filter)
    if status_filter == 'active':
        users_qs = users_qs.filter(is_active=True)
    elif status_filter == 'inactive':
        users_qs = users_qs.filter(is_active=False)

    paginator = Paginator(users_qs, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'query': query,
        'role_filter': role_filter,
        'org_filter': org_filter,
        'status_filter': status_filter,
        'roles': USER_ROLE_CHOICES,
        'organizations': Organization.objects.filter(is_active=True),
        'total_users': users_qs.count(),
    }
    return render(request, 'accounts/user_list.html', context)


@login_required
@role_required(['super_admin', 'organization_admin'])
def user_create_view(request):
    """
    Administrative creation of enterprise accounts with role assignment.
    """
    if request.method == 'POST':
        form = AdminUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            log_audit_event(
                action='CREATE',
                module='accounts',
                object_id=user.pk,
                object_repr=user.username,
                description=f"Admin created account for {user.username} with role {user.get_role_display()}",
                request=request
            )
            messages.success(request, f"User account '{user.username}' created successfully.")
            return redirect('accounts:user_list')
    else:
        form = AdminUserCreateForm()

    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Create Enterprise User'})


@login_required
@role_required(['super_admin', 'organization_admin'])
def user_edit_view(request, pk):
    """
    Administrative editing of enterprise accounts.
    """
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = AdminUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            log_audit_event(
                action='UPDATE',
                module='accounts',
                object_id=user.pk,
                object_repr=user.username,
                description=f"Admin updated account details for {user.username}",
                request=request
            )
            messages.success(request, f"User '{user.username}' updated successfully.")
            return redirect('accounts:user_list')
    else:
        form = AdminUserUpdateForm(instance=user)

    return render(request, 'accounts/user_form.html', {'form': form, 'title': f'Edit User: {user.username}', 'target_user': user})


@login_required
@role_required(['super_admin', 'organization_admin'])
def user_toggle_status_view(request, pk):
    """
    Toggle user active/inactive status.
    """
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, "You cannot deactivate your own administrative account.")
        return redirect('accounts:user_list')

    user.is_active = not user.is_active
    user.save(update_fields=['is_active'])
    
    status_str = "activated" if user.is_active else "deactivated"
    log_audit_event(
        action='UPDATE',
        module='accounts',
        object_id=user.pk,
        object_repr=user.username,
        description=f"Admin {status_str} user account {user.username}",
        request=request
    )
    messages.success(request, f"User account '{user.username}' has been {status_str}.")
    return redirect('accounts:user_list')
