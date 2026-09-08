from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q, Sum, Count

from .models import Expense
from .forms import ExpenseForm
from apps.permissions.decorators import permission_required
from apps.audit.utils import log_audit_event

@login_required
def expense_list_view(request):
    """
    Financial expense vouchers listing with category, approval status, and project filters.
    """
    query = request.GET.get('q', '').strip()
    cat_filter = request.GET.get('category', '')
    status_filter = request.GET.get('status', '')

    expenses_qs = Expense.objects.select_related('asset', 'project', 'work_order', 'contractor', 'approved_by').all()

    if query:
        expenses_qs = expenses_qs.filter(
            Q(expense_id__icontains=query) |
            Q(description__icontains=query) |
            Q(invoice_number__icontains=query) |
            Q(contractor__company_name__icontains=query)
        )
    if cat_filter:
        expenses_qs = expenses_qs.filter(category=cat_filter)
    if status_filter:
        expenses_qs = expenses_qs.filter(approval_status=status_filter)

    total_amount = expenses_qs.aggregate(total=Sum('amount'))['total'] or 0
    approved_amount = expenses_qs.filter(approval_status='APPROVED').aggregate(total=Sum('amount'))['total'] or 0

    paginator = Paginator(expenses_qs, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'query': query,
        'cat_filter': cat_filter,
        'status_filter': status_filter,
        'categories': Expense.CATEGORY_CHOICES,
        'statuses': Expense.APPROVAL_STATUS_CHOICES,
        'total_expenses': expenses_qs.count(),
        'total_amount': total_amount,
        'approved_amount': approved_amount,
        'pending_count': expenses_qs.filter(approval_status='PENDING').count(),
    }
    return render(request, 'expenses/expense_list.html', context)


@login_required
def expense_detail_view(request, pk):
    """
    Expense voucher dossier with linked invoice attachment and approval chain.
    """
    expense = get_object_or_404(
        Expense.objects.select_related('asset', 'project', 'work_order', 'contractor', 'approved_by'),
        pk=pk
    )
    return render(request, 'expenses/expense_detail.html', {'expense': expense})


@login_required
@permission_required('expenses', 'create')
def expense_create_view(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            exp = form.save()
            log_audit_event(
                action='BUDGET_ACTION',
                module='expenses',
                object_id=exp.pk,
                object_repr=f"{exp.expense_id} (${exp.amount})",
                description=f"Logged expense voucher {exp.expense_id} for ${exp.amount}",
                request=request
            )
            messages.success(request, f"Expense voucher '{exp.expense_id}' recorded successfully.")
            return redirect('expenses:detail', pk=exp.pk)
    else:
        form = ExpenseForm()
    return render(request, 'expenses/expense_form.html', {'form': form, 'title': 'Record Expense Voucher'})


@login_required
@permission_required('expenses', 'edit')
def expense_update_view(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES, instance=expense)
        if form.is_valid():
            exp = form.save()
            log_audit_event(
                action='UPDATE',
                module='expenses',
                object_id=exp.pk,
                object_repr=exp.expense_id,
                description=f"Updated expense record {exp.expense_id}",
                request=request
            )
            messages.success(request, f"Expense voucher '{exp.expense_id}' updated.")
            return redirect('expenses:detail', pk=exp.pk)
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/expense_form.html', {'form': form, 'title': f'Edit Expense: {expense.expense_id}', 'expense': expense})


@login_required
@permission_required('expenses', 'approve')
def expense_approve_view(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.approval_status = 'APPROVED'
    expense.approved_by = request.user
    expense.approved_at = timezone.now()
    expense.save(update_fields=['approval_status', 'approved_by', 'approved_at'])

    # Update project or budget actual spend if linked
    if expense.project:
        expense.project.actual_spending += expense.amount
        expense.project.save(update_fields=['actual_spending'])

    log_audit_event(
        action='BUDGET_ACTION',
        module='expenses',
        object_id=expense.pk,
        object_repr=expense.expense_id,
        description=f"Approved expense voucher {expense.expense_id} for ${expense.amount}",
        request=request
    )
    messages.success(request, f"Expense voucher '{expense.expense_id}' approved.")
    return redirect('expenses:detail', pk=expense.pk)
