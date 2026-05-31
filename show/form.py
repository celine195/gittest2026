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
        }
    
    def clean(self):
        cleaned_data = super().clean()
        
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        periods_start = cleaned_data.get('periods')
        periods_end = cleaned_data.get('periods_end')
        
    
        device_type = cleaned_data.get('device_type')
        
        
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
            
            for vehicle in all_vehicles:
          
                is_occupied = Borrowlist.objects.filter(
                    start_date=start_date,
                    periods=periods_start,
                    assigned_vehicle=vehicle
                ).exclude(status='已拒絕').exists()
                
                if not is_occupied:
                    assigned_success = True
                    break  
            
            
            if not assigned_success:
                raise forms.ValidationError("❌ 很抱歉，該時段的此種類行動載具車已被預約一空，請選擇其他時段！")


        return cleaned_data




