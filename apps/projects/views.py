from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Avg, Count

from .models import Project, ProjectMilestone
from .forms import ProjectForm, ProjectMilestoneForm
from apps.permissions.decorators import permission_required
from apps.audit.utils import log_audit_event

@login_required
def project_list_view(request):
    """
    Capital projects directory with budget utilization and Gantt tracking.
    """
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '')

    projects_qs = Project.objects.select_related(
        'organization', 'project_manager', 'contractor'
    ).annotate(milestone_count=Count('milestones'))

    if query:
        projects_qs = projects_qs.filter(
            Q(project_id__icontains=query) |
            Q(name__icontains=query) |
            Q(contractor__company_name__icontains=query)
        )
    if status_filter:
        projects_qs = projects_qs.filter(status=status_filter)

    total_budget = projects_qs.aggregate(total=Sum('budget'))['total'] or 0
    total_spent = projects_qs.aggregate(total=Sum('actual_spending'))['total'] or 0
    avg_progress = projects_qs.aggregate(avg=Avg('progress'))['avg'] or 0

    paginator = Paginator(projects_qs, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'query': query,
        'status_filter': status_filter,
        'statuses': Project.STATUS_CHOICES,
        'total_projects': projects_qs.count(),
        'total_budget': total_budget,
        'total_spent': total_spent,
        'avg_progress': round(avg_progress, 1),
    }
    return render(request, 'projects/project_list.html', context)


@login_required
def project_detail_view(request, pk):
    """
    Project capital dashboard, WBS milestones, contractor performance, and expense logs.
    """
    project = get_object_or_404(
        Project.objects.select_related('organization', 'project_manager', 'contractor'),
        pk=pk
    )
    milestones = project.milestones.all()
    expenses = project.expenses.all()[:15] if hasattr(project, 'expenses') else []
    documents = project.documents.all()[:10] if hasattr(project, 'documents') else []

    context = {
        'project': project,
        'milestones': milestones,
        'expenses': expenses,
        'documents': documents,
    }
    return render(request, 'projects/project_detail.html', context)


@login_required
@permission_required('projects', 'create')
def project_create_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            prj = form.save()
            log_audit_event(
                action='CREATE',
                module='projects',
                object_id=prj.pk,
                object_repr=f"{prj.project_id} ({prj.name})",
                description=f"Initiated capital project {prj.name} with budget ${prj.budget}",
                request=request
            )
            messages.success(request, f"Project '{prj.name}' created successfully.")
            return redirect('projects:detail', pk=prj.pk)
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form, 'title': 'Create Capital Project'})


@login_required
@permission_required('projects', 'edit')
def project_update_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            prj = form.save()
            log_audit_event(
                action='PROJECT_CHANGE',
                module='projects',
                object_id=prj.pk,
                object_repr=prj.project_id,
                description=f"Updated progress to {prj.progress}% for project {prj.project_id}",
                request=request
            )
            messages.success(request, f"Project '{prj.name}' updated.")
            return redirect('projects:detail', pk=prj.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_form.html', {'form': form, 'title': f'Edit Project: {project.name}', 'project': project})


@login_required
@permission_required('projects', 'create')
def project_add_milestone_view(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if request.method == 'POST':
        form = ProjectMilestoneForm(request.POST)
        if form.is_valid():
            ms = form.save(commit=False)
            ms.project = project
            ms.save()
            messages.success(request, f"Milestone '{ms.milestone_title}' added.")
            return redirect('projects:detail', pk=project.pk)
    else:
        form = ProjectMilestoneForm()
    return render(request, 'projects/generic_form.html', {'form': form, 'title': f'Add Milestone for {project.name}'})


@login_required
def project_gantt_view(request):
    """
    Enterprise Gantt timeline visualization for all active capital projects.
    """
    projects = Project.objects.filter(status__in=['APPROVED', 'ACTIVE', 'DELAYED']).prefetch_related('milestones')
    return render(request, 'projects/gantt_view.html', {'projects': projects})
