from django.db import models
from django.contrib.auth.models import User 
from django import forms


class CustomRegistrationForm(forms.ModelForm):
    ROLE_CHOICES = (
        ('teacher', '老師'),
        ('administrator','圖書館管理員'),
        ('student', '學生'),
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='student')

    class Meta:
        model = User
        fields = ['username', 'email'] 

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        self.role = cleaned_data.get("role")
        if password != confirm_password:
            raise forms.ValidationError("兩次輸入的密碼不一致！")
        return cleaned_data

class device(models.Model):
    DEVICE_CHOICES =(
        ('ipad', 'iPad'),
        ('chromebook', 'Chromebook'),
        ('surface_go', 'Surface Go'),
        ('acer_laptop', 'Acer 小筆電'),
    )
    device_type = models.CharField("載具種類", max_length=20, choices=DEVICE_CHOICES, unique=True)

    def __str__(self):
        return f"{self.device_type} - {self.id}"

class Borrowlist(models.Model):

    user = models.CharField("借用老師",max_length=20)
    phone = models.CharField("聯絡電話", max_length=25)
    location = models.CharField("教室", max_length=10)

    usage_type_choices = (
        ('once','單次'),
        ('weekly','每周'),
    )


    start_date = models.DateField("開始日期", null=True, blank=True)
    end_date = models.DateField("結束日期", null=True, blank=True)
    
    DAY_CHOICES = (
        ('Monday','星期一'), ('Tuesday','星期二'), ('Wednesday','星期三'),
        ('Thursday','星期四'), ('Friday','星期五'),
    )
    day = models.CharField("星期", choices=DAY_CHOICES, max_length=50, blank=True, null=True)

    PERIODS_CHOICES = (
        ('1', '第一節'), ('2', '第二節'), ('3', '第三節'), ('4', '第四節'),
        ('4.5', '午休'), ('5', '第五節'), ('6', '第六節'), ('7', '第七節'), ('8', '第八節'),
    )
    periods = models.CharField("預約節次", max_length=50, choices=PERIODS_CHOICES, default='1')

    STATUS_CHOICES = (
        ('待審核', '待審核'),
        ('已通過', '已通過'),
        ('已拒絕', '已拒絕'),
    )
    usage_type = models.CharField(max_length=10, choices = usage_type_choices , default='once')
    device_id = models.IntegerField()
    
    user = models.CharField("借用老師", max_length=20)
    device_id = models.ForeignKey('device', on_delete=models.CASCADE, verbose_name="載具")
    time_id = models.ForeignKey('time', on_delete=models.CASCADE, verbose_name="時間排程")
    status = models.CharField("審核狀態", max_length=10, choices = STATUS_CHOICES , default='待審核')
    
    device_amount = models.PositiveIntegerField(default=1)
    
    classroom = models.CharField(max_length = 10)
    
    
class time(models.Model):
    start_date = models.DateField("開始日期",null=True, blank=True)
    end_date = models.DateField("結束日期",null=True, blank=True)
    PERIODS_CHOICES = (
        ('1', '第一節'),
        ('2', '第二節'),
        ('3', '第三節'),
        ('4', '第四節'),
        ('5', '第五節'),
        ('6', '第六節'),
        ('7', '第七節'),
        ('8', '第八節'),
        ('4.5', '午休'),
    )
    periods = models.CharField(
        max_length=50, 
        choices=PERIODS_CHOICES, 
        verbose_name="節次",
        default='1'
    )
    DAY_CHOICES = (
        ('Monday','星期一'),
        ('Tuesday','星期二'),
        ('Wednesday','星期三'),
        ('Thursday','星期四'),
        ('Friday','星期五'),
    )
    day = models.CharField(
        choices=DAY_CHOICES,
        max_length=50, 
        verbose_name="星期")



class devicecar(models.Model):
    device_id = models.CharField(
        max_length=100, 
        )
    device_amount = models.PositiveIntegerField(default=1)

class reservationlist(models.Model):
    list_id = models.IntegerField()
    date = models.DateField()
    time_id = models.IntegerField()
    device_id = models.IntegerField()
    devicecar_id = models.IntegerField()
    class Meta: 
        db_table = 'show_reservationlist'