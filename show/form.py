from django import forms
from .models import Borrowlist

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Borrowlist
        fields = ['user','phone', 'location', 'classroom', 'usage_type', 'start_date', 'end_date', 'day', 'periods', 'device_amount','device_type','exclude_weeks']
        exclude = ['user']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'day': forms.Select(attrs={'class': 'form-control'}),
            'periods': forms.Select(attrs={'class': 'form-control'}),
        }