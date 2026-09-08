from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count

from .models import Budget, BudgetAllocation
from .forms import BudgetForm, BudgetAllocationForm
from apps.permissions.decorators import permission_required
from apps.audit.utils import log_audit_event

@login_required
def budget_list_view(request):
    """
    Fiscal budget directory with utilization ratios and variance metrics.
    """
    query = request.GET.get('q', '').strip()
    type_filter = request.GET.get('type', '')
    year_filter = request.GET.get('year', '')

    budgets_qs = Budget.objects.select_related('organization', 'department').all()

    if query:
        budgets_qs = budgets_qs.filter(
            Q(budget_code__icontains=query) |
            Q(title__icontains=query) |
            Q(department__name__icontains=query)
        )
    if type_filter:
        budgets_qs = budgets_qs.filter(budget_type=type_filter)
    if year_filter:
        budgets_qs = budgets_qs.filter(fiscal_year=year_filter)

    total_allocated = budgets_qs.aggregate(total=Sum('allocated_amount'))['total'] or 0
    total_spent = budgets_qs.aggregate(total=Sum('spent_amount'))['total'] or 0
    total_remaining = total_allocated - total_spent
    overall_utilization = round((total_spent / total_allocated * 100), 1) if total_allocated > 0 else 0.0

    paginator = Paginator(budgets_qs, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'query': query,
        'type_filter': type_filter,
        'year_filter': year_filter,
        'budget_types': Budget.BUDGET_TYPES,
        'total_budgets': budgets_qs.count(),
        'total_allocated': total_allocated,
        'total_spent': total_spent,
        'total_remaining': total_remaining,
        'overall_utilization': overall_utilization,
    }
    return render(request, 'budgets/budget_list.html', context)


@login_required
def budget_detail_view(request, pk):
    """
    Detailed budget envelope dossier with category line-item allocations.
    """
    budget = get_object_or_404(Budget.objects.select_related('organization', 'department'), pk=pk)
    allocations = budget.allocations.all()

    context = {
        'budget': budget,
        'allocations': allocations,
    }
    return render(request, 'budgets/budget_detail.html', context)


@login_required
@permission_required('budgets', 'create')
def budget_create_view(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            bgt = form.save()
            log_audit_event(
                action='BUDGET_ACTION',
                module='budgets',
                object_id=bgt.pk,
                object_repr=f"{bgt.budget_code} ({bgt.title})",
                description=f"Authorized fiscal budget {bgt.title} for ${bgt.allocated_amount}",
                request=request
            )
            messages.success(request, f"Budget '{bgt.title}' registered successfully.")
            return redirect('budgets:detail', pk=bgt.pk)
    else:
        form = BudgetForm()
    return render(request, 'budgets/budget_form.html', {'form': form, 'title': 'Create Budget Allocation'})


@login_required
@permission_required('budgets', 'edit')
def budget_update_view(request, pk):
    budget = get_object_or_404(Budget, pk=pk)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            bgt = form.save()
            log_audit_event(
                action='BUDGET_ACTION',
                module='budgets',
                object_id=bgt.pk,
                object_repr=bgt.budget_code,
                description=f"Updated budget allocations for {bgt.budget_code}",
                request=request
            )
            messages.success(request, f"Budget '{bgt.title}' updated successfully.")
            return redirect('budgets:detail', pk=bgt.pk)
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'budgets/budget_form.html', {'form': form, 'title': f'Edit Budget: {budget.title}', 'budget': budget})


@login_required
@permission_required('budgets', 'create')
def budget_add_allocation_view(request, budget_pk):
    budget = get_object_or_404(Budget, pk=budget_pk)
    if request.method == 'POST':
        form = BudgetAllocationForm(request.POST)
        if form.is_valid():
            alloc = form.save(commit=False)
            alloc.budget = budget
            alloc.save()
            messages.success(request, f"Allocation line '{alloc.category_name}' added to budget.")
            return redirect('budgets:detail', pk=budget.pk)
    else:
        form = BudgetAllocationForm()
    return render(request, 'budgets/generic_form.html', {'form': form, 'title': f'Add Line Item Allocation for {budget.title}'})
