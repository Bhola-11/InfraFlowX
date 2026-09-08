from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import RolePermission, UserPermissionOverride, SYSTEM_MODULES
from .decorators import role_required

@login_required
@role_required(['super_admin', 'organization_admin'])
def permission_matrix_view(request):
    """
    Interactive enterprise security matrix management view.
    """
    from apps.accounts.models import USER_ROLE_CHOICES
    
    selected_role = request.GET.get('role', 'asset_manager')
    
    if request.method == 'POST':
        # Update permissions for selected role
        for module_key, _ in SYSTEM_MODULES:
            can_view = request.POST.get(f'perm_{module_key}_view') == 'on'
            can_create = request.POST.get(f'perm_{module_key}_create') == 'on'
            can_edit = request.POST.get(f'perm_{module_key}_edit') == 'on'
            can_delete = request.POST.get(f'perm_{module_key}_delete') == 'on'
            can_approve = request.POST.get(f'perm_{module_key}_approve') == 'on'
            can_export = request.POST.get(f'perm_{module_key}_export') == 'on'
            
            RolePermission.objects.update_or_create(
                role=selected_role,
                module=module_key,
                defaults={
                    'can_view': can_view,
                    'can_create': can_create,
                    'can_edit': can_edit,
                    'can_delete': can_delete,
                    'can_approve': can_approve,
                    'can_export': can_export,
                }
            )
        messages.success(request, f"Permissions successfully updated for role: {dict(USER_ROLE_CHOICES).get(selected_role, selected_role)}")
        return redirect(f"{request.path}?role={selected_role}")

    # Build matrix table data
    existing_perms = {
        rp.module: rp 
        for rp in RolePermission.objects.filter(role=selected_role)
    }

    matrix_rows = []
    for module_key, module_label in SYSTEM_MODULES:
        perm = existing_perms.get(module_key)
        matrix_rows.append({
            'module_key': module_key,
            'module_label': module_label,
            'can_view': perm.can_view if perm else True,
            'can_create': perm.can_create if perm else False,
            'can_edit': perm.can_edit if perm else False,
            'can_delete': perm.can_delete if perm else False,
            'can_approve': perm.can_approve if perm else False,
            'can_export': perm.can_export if perm else False,
        })

    context = {
        'roles': USER_ROLE_CHOICES,
        'selected_role': selected_role,
        'matrix_rows': matrix_rows,
        'selected_role_label': dict(USER_ROLE_CHOICES).get(selected_role, selected_role),
    }
    return render(request, 'permissions/matrix.html', context)
