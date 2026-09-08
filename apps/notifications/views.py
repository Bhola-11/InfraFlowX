from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Notification

@login_required
def notification_list_view(request):
    """
    User notification hub listing all notifications with filter by read/unread and category.
    """
    filter_type = request.GET.get('filter', 'all')
    notifications_qs = Notification.objects.filter(recipient=request.user)

    if filter_type == 'unread':
        notifications_qs = notifications_qs.filter(is_read=False)
    elif filter_type == 'read':
        notifications_qs = notifications_qs.filter(is_read=True)

    paginator = Paginator(notifications_qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'filter_type': filter_type,
        'total_count': Notification.objects.filter(recipient=request.user).count(),
        'unread_count': Notification.objects.filter(recipient=request.user, is_read=False).count(),
    }
    return render(request, 'notifications/notification_list.html', context)


@login_required
def mark_notification_read(request, pk):
    """
    Mark single notification as read and redirect to target action link or notification list.
    """
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    if not notification.is_read:
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'id': notification.pk})

    if notification.link:
        return redirect(notification.link)
    return redirect('notifications:list')


@login_required
def mark_all_notifications_read(request):
    """
    Mark all unread notifications for current user as read.
    """
    Notification.objects.filter(recipient=request.user, is_read=False).update(
        is_read=True,
        read_at=timezone.now()
    )
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    messages.success(request, "All notifications marked as read.")
    return redirect('notifications:list')
