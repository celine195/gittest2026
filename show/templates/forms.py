from django import forms
from .models import templates

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'phone',
            'usage_type',
            'start_date',
            'end_date',
            'periods',
            'exclude_weeks',
            'classroom',
            'device_type',
            'quantity',
        ]