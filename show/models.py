from django.db import models
from django.contrib.auth.models import User
from django import forms


class CustomRegistrationForm(forms.ModelForm):
    ROLE_CHOICES = (
        ('teacher', '一般老師'),
        ('admin', '圖書館管理員'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="申請身分", widget=forms.RadioSelect)
    password = forms.CharField(label="密碼", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="確認密碼", widget=forms.PasswordInput)

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

class list(models.Model):

    user = models.CharField("借用老師",max_length=20)
    phone = models.CharField("聯絡電話", max_length=25)
    location = models.CharField("教室", max_length=10)

    usage_type_choices = (
        ('once','單次'),
        ('weekly','每周'),
    )
    usage_type = models.CharField(max_length=10, choices=usage_type_choices, default='once')
    device_id = models.IntegerField()
    AMOUNT_CHOICES = (
        ('1', '1台'),
        ('2', '2台'),
        ('3', '3台'),
        ('4', '4台'),
        ('5', '5台'),
        ('6', '6台'),
        ('7', '7台'),
        ('8', '8台'),
        ('9', '9台'),
        ('10', '10台'),
        ('11', '11台'),
        ('12', '12台'),
        ('13', '13台'),
        ('14', '14台'),
        ('15', '15台'),
        ('16', '16台'),
        ('17', '17台'),
        ('18', '18台'),
        ('19', '19台'),
        ('20', '20台'),
        ('21', '21台'),
        ('22', '22台'),
        ('23', '23台'),
        ('24', '24台'),
        ('25', '25台'),
        ('26', '26台'),
        ('27', '27台'),
        ('28', '28台'),
        ('29', '29台'),
        ('30', '30台'),
        ('31', '31台'),
        ('32', '32台'),
        ('33', '33台'),
        ('34', '34台'),
        ('35', '35台'),
        ('one', '1車'),
        ('two', '2車'),
        ('three', '3車'),
        ('four', '4車'),
        ('five', '5車'),
    )
    device_amount = models.PositiveIntegerField(choices=AMOUNT_CHOICES, default=1)
    time_id = models.IntegerField
    classroom = models.CharField(max_length = 10)
    
    
class time(models.Model):
    start_date = models.DateField("開始日期",null=True, blank=True)
    end_date = models.DateField("結束日期",null=True, blank=True)
    PERIODS_CHOICES =(
        ('1','第一節'),
        ('2','第二節'),
        ('3','第三節'),
        ('4','第四節'),
        ('5','第五節'),
        ('6','第六節'),
        ('7','第七節'),
        ('8','第八節'),
        ('4.5','午休'),
    )
    period = models.CharField("借用節次", max_length=5, choices=PERIODS_CHOICES)

    start_date = models.DateField("開始日期")
    end_date = models.DateField("結束日期", help_text="若是單次借用，結束日期請設定與開始日期相同")
    excluded_weeks = models.CharField("不包含的週次/日期", max_length=200, blank=True, null=True, help_text="例如：第9週期中考、2026-05-20")

    BORROW_TYPE_CHOICES = (
        ('unit', '散借 (20台以內)'),
        ('car', '借用整台載具車'),
    )

    device_type = models.ForeignKey(device, on_delete=models.CASCADE, verbose_name="要借什麼載具")
    borrow_type = models.CharField("借用形式", max_length=10, choices=BORROW_TYPE_CHOICES, default='unit')
    quantity = models.PositiveIntegerField("借用數量", help_text="散借填寫台數，車借填寫車數")

    pickup_by = models.CharField("誰來拿", max_length=50, default="學生（帶學生證）")
    created_at = models.DateTimeField("填單時間", auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - {self.device_type} ({self.start_date})"

class devicecar(models.Model):
    device_type = models.ForeignKey(device, on_delete=models.CASCADE, verbose_name="所屬載具種類")
    car_code = models.CharField("車次代號", max_length=10, help_text="例如: B車")
    capacity = models.PositiveIntegerField("車內載具總台數", default=42)

    def __str__(self):
        return f"{self.device_type} - {self.car_code} ({self.capacity}台)"

class ReservationSchedule(models.Model):

    booking_form = models.ForeignKey(list, on_delete=models.CASCADE, verbose_name="對應的表單")
    date = models.DateField("借用當天日期")
    period = models.CharField("節次", max_length=5, choices=time.PERIODS_CHOICES)
    device_type = models.ForeignKey(device, on_delete=models.CASCADE, verbose_name="載具種類")
    
    # 排程防撞
    assigned_car = models.ForeignKey(devicecar, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="指派車次", help_text="若為散借則此處留空")
    is_scattered = models.BooleanField("是否為散借", default=False)
    borrowed_amount = models.PositiveIntegerField("實際借出載具數量")

    class Meta:
        verbose_name = "預約總表"
        unique_together = ('date', 'period', 'assigned_car')

    def __str__(self):
        car_info = self.assigned_car.car_code if self.assigned_car else "散裝"
        return f"{self.date} 第{self.period}節 - {self.device_type} [{car_info}] -> {self.booking_form.location}"