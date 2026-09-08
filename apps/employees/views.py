from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count

from .models import Designation, Skill, Certification, Employee, EmployeeSkill, EmployeeCertification
from .forms import (
    EmployeeForm, DesignationForm, SkillForm, CertificationForm,
    EmployeeSkillForm, EmployeeCertificationForm
)
from apps.organizations.models import Organization, Department
from apps.permissions.decorators import permission_required
from apps.audit.utils import log_audit_event

@login_required
def employee_list_view(request):
    """
    Enterprise staff directory with real-time filtering and status badges.
    """
    query = request.GET.get('q', '').strip()
    dept_filter = request.GET.get('dept', '')
    status_filter = request.GET.get('status', '')
    org_filter = request.GET.get('org', '')

    employees_qs = Employee.objects.select_related(
        'user', 'organization', 'department', 'designation', 'team', 'office'
    ).all()

    if query:
        employees_qs = employees_qs.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(employee_id__icontains=query) |
            Q(user__email__icontains=query) |
            Q(designation__title__icontains=query)
        )
    if dept_filter:
        employees_qs = employees_qs.filter(department_id=dept_filter)
    if status_filter:
        employees_qs = employees_qs.filter(status=status_filter)
    if org_filter:
        employees_qs = employees_qs.filter(organization_id=org_filter)

    paginator = Paginator(employees_qs, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'query': query,
        'dept_filter': dept_filter,
        'status_filter': status_filter,
        'org_filter': org_filter,
        'departments': Department.objects.all(),
        'organizations': Organization.objects.filter(is_active=True),
        'statuses': Employee.STATUS_CHOICES,
        'total_employees': employees_qs.count(),
    }
    return render(request, 'employees/employee_list.html', context)


@login_required
def employee_detail_view(request, pk):
    """
    Comprehensive employee profile showing skills, verified certifications, team assignments.
    """
    employee = get_object_or_404(
        Employee.objects.select_related('user', 'organization', 'department', 'designation', 'team', 'office', 'supervisor__user'),
        pk=pk
    )
    skills = employee.skills.select_related('skill').all()
    certifications = employee.certifications.select_related('certification').all()
    subordinates = employee.subordinates.select_related('user', 'designation').all()

    context = {
        'employee': employee,
        'skills': skills,
        'certifications': certifications,
        'subordinates': subordinates,
    }
    return render(request, 'employees/employee_detail.html', context)


@login_required
@permission_required('employees', 'create')
def employee_create_view(request):
    """
    Register a new employee profile.
    """
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            emp = form.save()
            log_audit_event(
                action='CREATE',
                module='employees',
                object_id=emp.pk,
                object_repr=f"{emp.user.get_full_name()} ({emp.employee_id})",
                description=f"Created employee record {emp.employee_id} for user {emp.user.username}",
                request=request
            )
            messages.success(request, f"Employee record for '{emp.user.get_full_name()}' created successfully.")
            return redirect('employees:detail', pk=emp.pk)
    else:
        form = EmployeeForm()

    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Add New Employee'})


@login_required
@permission_required('employees', 'edit')
def employee_update_view(request, pk):
    """
    Update employee profile information.
    """
    emp = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=emp)
        if form.is_valid():
            emp = form.save()
            log_audit_event(
                action='UPDATE',
                module='employees',
                object_id=emp.pk,
                object_repr=f"{emp.user.get_full_name()} ({emp.employee_id})",
                description=f"Updated employee record {emp.employee_id}",
                request=request
            )
            messages.success(request, f"Employee '{emp.user.get_full_name()}' updated successfully.")
            return redirect('employees:detail', pk=emp.pk)
    else:
        form = EmployeeForm(instance=emp)

    return render(request, 'employees/employee_form.html', {'form': form, 'title': f'Edit Employee: {emp.user.get_full_name()}', 'employee': emp})


# Skill Matrix & Certifications
@login_required
def skill_matrix_view(request):
    """
    Enterprise technical skill competency matrix.
    """
    skills = Skill.objects.annotate(employee_count=Count('certified_employees'))
    categories = Skill.CATEGORY_CHOICES
    return render(request, 'employees/skill_matrix.html', {'skills': skills, 'categories': categories})


@login_required
@permission_required('employees', 'create')
def skill_create_view(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save()
            messages.success(request, f"Skill '{skill.name}' added to competency registry.")
            return redirect('employees:skill_matrix')
    else:
        form = SkillForm()
    return render(request, 'employees/generic_form.html', {'form': form, 'title': 'Add New Skill Competency'})


@login_required
def designation_list_view(request):
    designations = Designation.objects.annotate(holder_count=Count('holders'))
    return render(request, 'employees/designation_list.html', {'designations': designations})


@login_required
@permission_required('employees', 'create')
def designation_create_view(request):
    if request.method == 'POST':
        form = DesignationForm(request.POST)
        if form.is_valid():
            desig = form.save()
            messages.success(request, f"Designation '{desig.title}' created.")
            return redirect('employees:designation_list')
    else:
        form = DesignationForm()
    return render(request, 'employees/generic_form.html', {'form': form, 'title': 'Add New Designation'})


@login_required
def certification_list_view(request):
    certs = Certification.objects.annotate(holder_count=Count('holders'))
    return render(request, 'employees/certification_list.html', {'certifications': certs})


@login_required
@permission_required('employees', 'create')
def certification_create_view(request):
    if request.method == 'POST':
        form = CertificationForm(request.POST)
        if form.is_valid():
            cert = form.save()
            messages.success(request, f"Certification '{cert.name}' registered.")
            return redirect('employees:certification_list')
    else:
        form = CertificationForm()
    return render(request, 'employees/generic_form.html', {'form': form, 'title': 'Register Professional Certification'})


@login_required
def add_employee_skill_view(request, employee_pk):
    employee = get_object_or_404(Employee, pk=employee_pk)
    if request.method == 'POST':
        form = EmployeeSkillForm(request.POST)
        if form.is_valid():
            emp_skill = form.save(commit=False)
            emp_skill.employee = employee
            emp_skill.save()
            messages.success(request, f"Skill '{emp_skill.skill.name}' assigned to {employee.user.get_full_name()}.")
            return redirect('employees:detail', pk=employee.pk)
    else:
        form = EmployeeSkillForm()
    return render(request, 'employees/generic_form.html', {'form': form, 'title': f'Add Skill for {employee.user.get_full_name()}'})


@login_required
def add_employee_certification_view(request, employee_pk):
    employee = get_object_or_404(Employee, pk=employee_pk)
    if request.method == 'POST':
        form = EmployeeCertificationForm(request.POST, request.FILES)
        if form.is_valid():
            emp_cert = form.save(commit=False)
            emp_cert.employee = employee
            emp_cert.save()
            messages.success(request, f"Certification '{emp_cert.certification.name}' added for {employee.user.get_full_name()}.")
            return redirect('employees:detail', pk=employee.pk)
    else:
        form = EmployeeCertificationForm()
    return render(request, 'employees/generic_form.html', {'form': form, 'title': f'Add Certification for {employee.user.get_full_name()}'})
