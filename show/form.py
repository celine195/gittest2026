from django import forms
from .models import Borrowlist, devicecar

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Borrowlist
        fields = ['user','phone', 'location', 'classroom', 'usage_type', 'start_date', 'end_date', 'day', 'periods', 'device_amount','device_type','periods_end','exclude_weeks']
        exclude = ['user']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'day': forms.Select(attrs={'class': 'form-control'}),
            'periods': forms.Select(attrs={'class': 'form-control'}),
            'periods_end': forms.Select(attrs={'class': 'form-control'}),
            'device_amount': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': '1', 
                'max': '40'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        periods_start = cleaned_data.get('periods')
        periods_end = cleaned_data.get('periods_end')
        device_type = cleaned_data.get('device_type')

        device_amount = cleaned_data.get('device_amount') or 0
        
  
        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError("錯誤：結束日期不能早於開始日期")
                
        if start_date == end_date and periods_start and periods_end:
            try:
                if float(periods_end) < float(periods_start):
                    raise forms.ValidationError("錯誤：當天借用的結束節次不能早於開始節次")
            except (ValueError, TypeError):
                if periods_end < periods_start:
                    raise forms.ValidationError("錯誤：當天借用的結束節次不能早於開始節次")

       
        if start_date and periods_start and device_type:
            all_vehicles = devicecar.objects.filter(device_type=device_type)
            assigned_success = False
            max_available_amount = 0  
            
            for vehicle in all_vehicles:
            
                from django.db.models import Sum
                already_borrowed = Borrowlist.objects.filter(
                    start_date=start_date,
                    periods=periods_start,
                    assigned_vehicle=vehicle
                ).exclude(status='已拒絕').aggregate(total=Sum('device_amount'))['total'] or 0
         
                remaining_devices = vehicle.device_amount - already_borrowed
                
                if remaining_devices > max_available_amount:
                    max_available_amount = remaining_devices
              
                if remaining_devices >= device_amount:
                    assigned_success = True
                    break 
            
            if not assigned_success:
                if max_available_amount > 0:
                    raise forms.ValidationError(f"❌ 數量超出上限！該時段此種類載具目前最多只剩 {max_available_amount} 台可用。")
                else:
                    raise forms.ValidationError("❌ 很抱歉，該時段的此種類行動載具車已被預約一空，請選擇其他時段！")

        return cleaned_data





