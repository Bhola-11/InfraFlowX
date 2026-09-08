from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import SupportTicket, TicketComment, CitizenFeedback, SLAPolicy
from .forms import SupportTicketForm, TicketCommentForm, CitizenFeedbackForm
from apps.audit.utils import log_audit_event


@login_required
def ticket_list_view(request):
    tickets = SupportTicket.objects.select_related('asset', 'location', 'assigned_to', 'assigned_department').all()
    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    priority = request.GET.get('priority', '').strip()
    category = request.GET.get('category', '').strip()

    if q:
        tickets = tickets.filter(Q(ticket_number__icontains=q) | Q(subject__icontains=q) | Q(reporter_name__icontains=q))
    if status:
        tickets = tickets.filter(status=status)
    if priority:
        tickets = tickets.filter(priority=priority)
    if category:
        tickets = tickets.filter(category=category)

    paginator = Paginator(tickets, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'support/ticket_list.html', {
        'page_obj': page_obj,
        'search_query': q,
        'selected_status': status,
        'selected_priority': priority,
        'selected_category': category,
        'statuses': SupportTicket.STATUS_CHOICES,
        'priorities': SupportTicket.PRIORITY_CHOICES,
        'categories': SupportTicket.CATEGORY_CHOICES,
        'total_tickets': tickets.count(),
    })


@login_required
def ticket_detail_view(request, pk):
    ticket = get_object_or_404(SupportTicket.objects.select_related('asset', 'location', 'assigned_to', 'assigned_department'), pk=pk)
    comments = ticket.comments.select_related('author').all()
    feedback = getattr(ticket, 'feedback', None)
    comment_form = TicketCommentForm()
    feedback_form = CitizenFeedbackForm() if not feedback else None

    return render(request, 'support/ticket_detail.html', {
        'ticket': ticket,
        'comments': comments,
        'feedback': feedback,
        'comment_form': comment_form,
        'feedback_form': feedback_form,
    })


@login_required
def ticket_create_view(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            if not ticket.ticket_number:
                ticket.ticket_number = f"TKT-{timezone.now().strftime('%Y%m%d%H%M')}"
            ticket.save()
            log_audit_event(request.user, 'CREATE', 'SupportTicket', str(ticket.id), f"Logged ticket {ticket.ticket_number} - {ticket.subject}")
            messages.success(request, f"Support Ticket '{ticket.ticket_number}' created.")
            return redirect('support:ticket_detail', pk=ticket.id)
    else:
        init_num = f"TKT-{timezone.now().strftime('%Y%m%d%H%M')}"
        form = SupportTicketForm(initial={'ticket_number': init_num, 'reporter_name': request.user.get_full_name() or request.user.username, 'reporter_email': request.user.email})
    return render(request, 'support/ticket_form.html', {'form': form, 'title': 'Create Support Ticket / Citizen Complaint'})


@login_required
def ticket_update_view(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)
    if request.method == 'POST':
        form = SupportTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            if ticket.status == 'RESOLVED' and not ticket.resolution_date:
                ticket.resolution_date = timezone.now()
            ticket.save()
            log_audit_event(request.user, 'UPDATE', 'SupportTicket', str(ticket.id), f"Updated ticket {ticket.ticket_number} to {ticket.status}")
            messages.success(request, f"Ticket '{ticket.ticket_number}' updated.")
            return redirect('support:ticket_detail', pk=ticket.id)
    else:
        form = SupportTicketForm(instance=ticket)
    return render(request, 'support/ticket_form.html', {'form': form, 'title': f'Edit Ticket - {ticket.ticket_number}', 'ticket': ticket})


@login_required
def ticket_comment_create_view(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)
    if request.method == 'POST':
        form = TicketCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.author_name = request.user.get_full_name() or request.user.username
            comment.save()
            messages.success(request, "Comment added.")
    return redirect('support:ticket_detail', pk=ticket.id)


@login_required
def ticket_feedback_create_view(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)
    if request.method == 'POST':
        form = CitizenFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.ticket = ticket
            feedback.save()
            messages.success(request, "Feedback submitted. Thank you!")
    return redirect('support:ticket_detail', pk=ticket.id)


@login_required
def sla_policy_list_view(request):
    policies = SLAPolicy.objects.all()
    return render(request, 'support/sla_policies.html', {'policies': policies})
