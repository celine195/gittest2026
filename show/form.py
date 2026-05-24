from django import forms
from .models import Borrowlist, device, time


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Borrowlist
        fields = "__all__"

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

