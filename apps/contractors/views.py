from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg, Sum

from .models import Contractor, ContractAgreement, ContractorEvaluation
from .forms import ContractorForm, ContractAgreementForm, ContractorEvaluationForm
from apps.permissions.decorators import permission_required
from apps.audit.utils import log_audit_event

@login_required
def contractor_list_view(request):
    """
    Contractor vendor directory with SLA ratings, specializations and active agreement indicators.
    """
    query = request.GET.get('q', '').strip()
    spec_filter = request.GET.get('spec', '')
    status_filter = request.GET.get('status', '')

    contractors_qs = Contractor.objects.select_related('organization').annotate(
        contract_count=Count('agreements'),
        work_order_count=Count('work_orders') if hasattr(Contractor, 'work_orders') else Count('agreements')
    )

    if query:
        contractors_qs = contractors_qs.filter(
            Q(company_name__icontains=query) |
            Q(registration_number__icontains=query) |
            Q(contact_person__icontains=query)
        )
    if spec_filter:
        contractors_qs = contractors_qs.filter(specialization=spec_filter)
    if status_filter:
        contractors_qs = contractors_qs.filter(status=status_filter)

    avg_rating = contractors_qs.aggregate(avg=Avg('rating'))['avg'] or 0

    paginator = Paginator(contractors_qs, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'query': query,
        'spec_filter': spec_filter,
        'status_filter': status_filter,
        'specializations': Contractor.SPECIALIZATION_CHOICES,
        'statuses': Contractor.STATUS_CHOICES,
        'total_contractors': contractors_qs.count(),
        'avg_rating': round(avg_rating, 2),
    }
    return render(request, 'contractors/contractor_list.html', context)


@login_required
def contractor_detail_view(request, pk):
    """
    Contractor vendor dossier, active agreements, SLA evaluations, linked work orders and projects.
    """
    contractor = get_object_or_404(Contractor.objects.select_related('organization'), pk=pk)
    agreements = contractor.agreements.all()
    evaluations = contractor.evaluations.all()[:10]
    
    # Linked operational orders
    work_orders = contractor.work_orders.all()[:10] if hasattr(contractor, 'work_orders') else []
    projects = contractor.projects.all()[:10] if hasattr(contractor, 'projects') else []

    context = {
        'contractor': contractor,
        'agreements': agreements,
        'evaluations': evaluations,
        'work_orders': work_orders,
        'projects': projects,
    }
    return render(request, 'contractors/contractor_detail.html', context)


@login_required
@permission_required('contractors', 'create')
def contractor_create_view(request):
    if request.method == 'POST':
        form = ContractorForm(request.POST)
        if form.is_valid():
            contractor = form.save()
            log_audit_event(
                action='CREATE',
                module='contractors',
                object_id=contractor.pk,
                object_repr=contractor.company_name,
                description=f"Registered vendor contractor {contractor.company_name}",
                request=request
            )
            messages.success(request, f"Contractor '{contractor.company_name}' registered successfully.")
            return redirect('contractors:detail', pk=contractor.pk)
    else:
        form = ContractorForm()
    return render(request, 'contractors/contractor_form.html', {'form': form, 'title': 'Register Contractor Vendor'})


@login_required
@permission_required('contractors', 'edit')
def contractor_update_view(request, pk):
    contractor = get_object_or_404(Contractor, pk=pk)
    if request.method == 'POST':
        form = ContractorForm(request.POST, instance=contractor)
        if form.is_valid():
            contractor = form.save()
            log_audit_event(
                action='UPDATE',
                module='contractors',
                object_id=contractor.pk,
                object_repr=contractor.company_name,
                description=f"Updated parameters for contractor {contractor.company_name}",
                request=request
            )
            messages.success(request, f"Contractor '{contractor.company_name}' updated.")
            return redirect('contractors:detail', pk=contractor.pk)
    else:
        form = ContractorForm(instance=contractor)
    return render(request, 'contractors/contractor_form.html', {'form': form, 'title': f'Edit Contractor: {contractor.company_name}', 'contractor': contractor})


@login_required
@permission_required('contractors', 'create')
def contract_agreement_create_view(request, contractor_pk):
    contractor = get_object_or_404(Contractor, pk=contractor_pk)
    if request.method == 'POST':
        form = ContractAgreementForm(request.POST, request.FILES)
        if form.is_valid():
            agreement = form.save()
            messages.success(request, f"Contract agreement '{agreement.contract_title}' registered.")
            return redirect('contractors:detail', pk=contractor.pk)
    else:
        form = ContractAgreementForm(initial={'contractor': contractor, 'organization': contractor.organization})
    return render(request, 'contractors/generic_form.html', {'form': form, 'title': f'Add Contract Agreement for {contractor.company_name}'})


@login_required
@permission_required('contractors', 'edit')
def contractor_evaluation_create_view(request, contractor_pk):
    contractor = get_object_or_404(Contractor, pk=contractor_pk)
    if request.method == 'POST':
        form = ContractorEvaluationForm(request.POST)
        if form.is_valid():
            eval_obj = form.save(commit=False)
            eval_obj.contractor = contractor
            eval_obj.evaluated_by = request.user
            # Compute average score
            overall = (eval_obj.quality_score + eval_obj.safety_score + eval_obj.timeliness_score) / 3.0
            eval_obj.overall_score = round(overall, 2)
            eval_obj.save()

            # Recalculate contractor master rating
            all_evals = contractor.evaluations.all()
            avg_all = all_evals.aggregate(avg=Avg('overall_score'))['avg'] or 4.5
            contractor.rating = round(avg_all, 2)
            contractor.save(update_fields=['rating'])

            messages.success(request, f"SLA evaluation for {contractor.company_name} saved.")
            return redirect('contractors:detail', pk=contractor.pk)
    else:
        form = ContractorEvaluationForm(initial={'contractor': contractor})
    return render(request, 'contractors/generic_form.html', {'form': form, 'title': f'Conduct SLA Evaluation for {contractor.company_name}'})
