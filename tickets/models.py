from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError


class Ticket(models.Model):
    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_HIGH, 'High'),
    ]

    CATEGORY_TECH = 'technical'
    CATEGORY_BILLING = 'billing'
    CATEGORY_GENERAL = 'general'
    CATEGORY_CHOICES = [
        (CATEGORY_TECH, 'Technical'),
        (CATEGORY_BILLING, 'Billing'),
        (CATEGORY_GENERAL, 'General'),
    ]

    STATUS_OPEN = 'open'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_RESOLVED = 'resolved'
    STATUS_CLOSED = 'closed'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Open'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_RESOLVED, 'Resolved'),
        (STATUS_CLOSED, 'Closed'),
    ]

    subject = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=CATEGORY_GENERAL)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.get_priority_display()}] {self.subject} ({self.get_status_display()})"

    def clean(self):
        if not self.subject or len(self.subject.strip()) < 5:
            raise ValidationError({'subject': 'Subject must be at least 5 characters long.'})
        if self.status not in dict(self.STATUS_CHOICES):
            raise ValidationError({'status': 'Invalid status value.'})


class Reply(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='replies')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.message or not self.message.strip():
            raise ValidationError({'message': 'Reply cannot be empty.'})
        if self.ticket.status == Ticket.STATUS_CLOSED:
            raise ValidationError('Cannot add replies to a closed ticket.')

    def __str__(self):
        return f"Reply by {self.user} on {self.ticket}"
