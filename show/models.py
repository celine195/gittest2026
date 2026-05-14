from django.db import models
from datetime import timedelta

# Create your models here.

class user(models.Model):
    name = models.CharField("姓名",max_length= 10)
    email = models.CharField("信箱",max_length= 100)
    ROLE_CHOICES = (
        ('teacher', '老師'),
        ('student', '學生'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

#這裡我不確定如何引用學校帳號(身分、姓名等)，查到的方法感覺也不太合適，暫時先這樣

class list(models.Model):
    user_id = models.IntegerField("借用人")
    phone = models.CharField("連絡電話",max_length= 25)

    #這
    usage_type_choices = (
        ('once','單次'),
        ('weekly','每周'),
    )
    usage_type = models.CharField(max_length=10, choices=usage_type_choices, default='once')
    start_date = models.DateField("開始日期",null=True, blank=True)
    end_date = models.DateField("結束日期",null=True, blank=True)
    periods1 = models.BooleanField("第一節",default=False)
    periods2 = models.BooleanField("第二節",default=False)
    periods3 = models.BooleanField("第三節",default=False)
    periods4 = models.BooleanField("第四節",default=False)
    periods5 = models.BooleanField("第五節",default=False)
    periods6 = models.BooleanField("第六節",default=False)
    periods7 = models.BooleanField("第七節",default=False)
    periods8 = models.BooleanField("第八節",default=False)
    periodsbreak = models.BooleanField("午休",default=False)
    exclude_weeks_start = models.DateField()
    @property
    def end_date(self):
        return self.start_date + timedelta(days=6)
    #時間這邊感覺要整個重寫，感覺可以拉出來額外填寫一個model