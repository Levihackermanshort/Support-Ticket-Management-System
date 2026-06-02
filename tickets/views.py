from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket, Reply
from .forms import TicketForm, ReplyForm
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.mail import send_mail


@login_required
def dashboard(request):
    total = Ticket.objects.count()
    open_count = Ticket.objects.filter(status=Ticket.STATUS_OPEN).count()
    resolved = Ticket.objects.filter(status=Ticket.STATUS_RESOLVED).count()
    high_priority = Ticket.objects.filter(priority=Ticket.PRIORITY_HIGH).count()
    context = {
        'total': total,
        'open_count': open_count,
        'resolved': resolved,
        'high_priority': high_priority,
    }
    return render(request, 'tickets/dashboard.html', context)


@login_required
def ticket_list(request):
    qs = Ticket.objects.all().order_by('-created_at')
    q = request.GET.get('q')
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    if q:
        qs = qs.filter(subject__icontains=q)
    if status:
        qs = qs.filter(status=status)
    if priority:
        qs = qs.filter(priority=priority)

    paginator = Paginator(qs, 10)
    page = request.GET.get('page')
    try:
        tickets_page = paginator.page(page)
    except PageNotAnInteger:
        tickets_page = paginator.page(1)
    except EmptyPage:
        tickets_page = paginator.page(paginator.num_pages)

    return render(request, 'tickets/list.html', {'tickets': tickets_page, 'ticket_model': Ticket})


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    replies_qs = ticket.replies.order_by('created_at')
    paginator = Paginator(replies_qs, 5)
    page = request.GET.get('rpage')
    try:
        replies = paginator.page(page)
    except PageNotAnInteger:
        replies = paginator.page(1)
    except EmptyPage:
        replies = paginator.page(paginator.num_pages)

    form = ReplyForm()
    return render(request, 'tickets/detail.html', {'ticket': ticket, 'replies': replies, 'form': form})


@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            messages.success(request, 'Ticket created.')
            try:
                send_mail(
                    f"New ticket created: {ticket.subject}",
                    ticket.description,
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email] if request.user.email else [],
                    fail_silently=True,
                )
            except Exception:
                pass
            return redirect('tickets:detail', pk=ticket.pk)
    else:
        form = TicketForm()
    return render(request, 'tickets/form.html', {'form': form})


@login_required
def ticket_edit(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if ticket.created_by != request.user:
        messages.error(request, 'You can only edit your own tickets.')
        return redirect('tickets:detail', pk=pk)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ticket updated.')
            return redirect('tickets:detail', pk=pk)
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'tickets/form.html', {'form': form, 'ticket': ticket})


@login_required
def ticket_delete(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if ticket.created_by != request.user:
        messages.error(request, 'You can only delete your own tickets.')
        return redirect('tickets:detail', pk=pk)
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, 'Ticket deleted.')
        return redirect('tickets:list')
    return render(request, 'tickets/confirm_delete.html', {'ticket': ticket})


@login_required
def add_reply(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if ticket.status == Ticket.STATUS_CLOSED:
        messages.error(request, 'Cannot reply to a closed ticket.')
        return redirect('tickets:detail', pk=pk)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.ticket = ticket
            reply.user = request.user
            try:
                reply.full_clean()
                reply.save()
                messages.success(request, 'Reply added.')
                try:
                    send_mail(
                        f"New reply on ticket: {ticket.subject}",
                        reply.message,
                        settings.DEFAULT_FROM_EMAIL,
                        [ticket.created_by.email] if ticket.created_by.email else [],
                        fail_silently=True,
                    )
                except Exception:
                    pass
            except Exception as e:
                messages.error(request, str(e))
    return redirect('tickets:detail', pk=pk)
