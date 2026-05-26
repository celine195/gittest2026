from django import forms
from .models import Borrowlist, device, time


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Borrowlist
        fields = ['phone', 'location', 'classroom', 'usage_type', 'start_date', 'end_date', 'day', 'periods', 'device_amount']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'day': forms.Select(attrs={'class': 'form-control'}),
            'periods': forms.Select(attrs={'class': 'form-control'}),
        }

class DeviceForm(forms.ModelForm):
    class Meta:
        model = device
        fields = ['device_type']

class TimeForm(forms.ModelForm):
     class Meta:
        model = time
        fields = "__all__"
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }