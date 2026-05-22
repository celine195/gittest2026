from django import forms
from .models import list as BorrowList

class BorrowForm(forms.ModelForm):
    class Meta:
        model = BorrowList
        # 這裡列出要讓教師在畫面上填寫的欄位
        fields = ['phone', 'usage_type', 'classroom', 'device_type', 'quantity']