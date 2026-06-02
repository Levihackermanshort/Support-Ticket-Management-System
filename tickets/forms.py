from django import forms
from .models import Ticket, Reply


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'description', 'priority', 'category', 'status']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['message']

    def clean_message(self):
        data = self.cleaned_data.get('message', '')
        if not data.strip():
            raise forms.ValidationError('Reply cannot be empty.')
        return data
