from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Sum, Q

from .models import Organization, Region, Zone, Department, Office, Team
from .forms import OrganizationForm, RegionForm, ZoneForm, DepartmentForm, OfficeForm, TeamForm
from apps.permissions.decorators import permission_required, role_required
from apps.audit.utils import log_audit_event

@login_required
def organization_list_view(request):
    """
    Overview list of all enterprise organizations with summary stats.
    """
    query = request.GET.get('q', '').strip()
    orgs = Organization.objects.annotate(
        region_count=Count('regions', distinct=True),
        dept_count=Count('departments', distinct=True),
        office_count=Count('offices', distinct=True),
        member_count=Count('members', distinct=True),
    )
    if query:
        orgs = orgs.filter(Q(name__icontains=query) | Q(code__icontains=query))

    paginator = Paginator(orgs, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'query': query,
        'total_orgs': orgs.count(),
        'total_budget': Organization.objects.aggregate(total=Sum('annual_budget'))['total'] or 0,
    }
    return render(request, 'organizations/org_list.html', context)


@login_required
def organization_detail_view(request, pk):
    """
    In-depth organization profile showing departments, regions, teams, and executive members.
    """
    org = get_object_or_404(Organization, pk=pk)
    regions = org.regions.prefetch_related('zones').all()
    departments = org.departments.prefetch_related('teams').all()
    offices = org.offices.all()
    members = org.members.all()[:15]

    context = {
        'org': org,
        'regions': regions,
        'departments': departments,
        'offices': offices,
        'members': members,
    }
    return render(request, 'organizations/org_detail.html', context)


@login_required
@permission_required('organizations', 'create')
def organization_create_view(request):
    """
    Create a new enterprise organization.
    """
    if request.method == 'POST':
        form = OrganizationForm(request.POST, request.FILES)
        if form.is_valid():
            org = form.save()
            log_audit_event(
                action='CREATE',
                module='organizations',
                object_id=org.pk,
                object_repr=org.name,
                description=f"Created organization {org.name} ({org.code})",
                request=request
            )
            messages.success(request, f"Organization '{org.name}' successfully registered.")
            return redirect('organizations:detail', pk=org.pk)
    else:
        form = OrganizationForm()
    return render(request, 'organizations/org_form.html', {'form': form, 'title': 'Create Organization'})


@login_required
@permission_required('organizations', 'edit')
def organization_update_view(request, pk):
    """
    Update organization settings and budgets.
    """
    org = get_object_or_404(Organization, pk=pk)
    if request.method == 'POST':
        form = OrganizationForm(request.POST, request.FILES, instance=org)
        if form.is_valid():
            org = form.save()
            log_audit_event(
                action='UPDATE',
                module='organizations',
                object_id=org.pk,
                object_repr=org.name,
                description=f"Updated organization settings for {org.name}",
                request=request
            )
            messages.success(request, f"Organization '{org.name}' updated successfully.")
            return redirect('organizations:detail', pk=org.pk)
    else:
        form = OrganizationForm(instance=org)
    return render(request, 'organizations/org_form.html', {'form': form, 'title': f'Edit {org.name}', 'org': org})


@login_required
def organization_hierarchy_tree_view(request, pk=None):
    """
    Interactive visual hierarchy tree of Organization -> Regions -> Zones -> Offices & Departments -> Teams.
    """
    if pk:
        orgs = Organization.objects.filter(pk=pk).prefetch_related('regions__zones', 'departments__teams', 'offices')
    else:
        orgs = Organization.objects.all().prefetch_related('regions__zones', 'departments__teams', 'offices')

    context = {
        'orgs': orgs,
        'selected_org_id': str(pk) if pk else None,
    }
    return render(request, 'organizations/hierarchy_tree.html', context)


# Region Views
@login_required
def region_list_view(request):
    regions = Region.objects.select_related('organization', 'regional_head').annotate(zone_count=Count('zones'))
    return render(request, 'organizations/region_list.html', {'regions': regions})

@login_required
@permission_required('organizations', 'create')
def region_create_view(request):
    if request.method == 'POST':
        form = RegionForm(request.POST)
        if form.is_valid():
            region = form.save()
            messages.success(request, f"Region '{region.name}' created.")
            return redirect('organizations:region_list')
    else:
        form = RegionForm()
    return render(request, 'organizations/generic_form.html', {'form': form, 'title': 'Add New Region'})


# Department Views
@login_required
def department_list_view(request):
    departments = Department.objects.select_related('organization', 'head_of_department').annotate(team_count=Count('teams'))
    return render(request, 'organizations/department_list.html', {'departments': departments})

@login_required
@permission_required('organizations', 'create')
def department_create_view(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            dept = form.save()
            messages.success(request, f"Department '{dept.name}' created.")
            return redirect('organizations:department_list')
    else:
        form = DepartmentForm()
    return render(request, 'organizations/generic_form.html', {'form': form, 'title': 'Add New Department'})


# Office Views
@login_required
def office_list_view(request):
    offices = Office.objects.select_related('organization', 'region').all()
    return render(request, 'organizations/office_list.html', {'offices': offices})

@login_required
@permission_required('organizations', 'create')
def office_create_view(request):
    if request.method == 'POST':
        form = OfficeForm(request.POST)
        if form.is_valid():
            office = form.save()
            messages.success(request, f"Office '{office.name}' registered.")
            return redirect('organizations:office_list')
    else:
        form = OfficeForm()
    return render(request, 'organizations/generic_form.html', {'form': form, 'title': 'Register New Office'})


# Team Views
@login_required
def team_list_view(request):
    teams = Team.objects.select_related('department__organization', 'team_lead', 'office').all()
    return render(request, 'organizations/team_list.html', {'teams': teams})

@login_required
@permission_required('organizations', 'create')
def team_create_view(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            messages.success(request, f"Team '{team.name}' registered.")
            return redirect('organizations:team_list')
    else:
        form = TeamForm()
    return render(request, 'organizations/generic_form.html', {'form': form, 'title': 'Register New Team'})
