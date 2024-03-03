from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['location', 'activities', 'estimated_cost', 'start_time', 'end_time', 'date']
