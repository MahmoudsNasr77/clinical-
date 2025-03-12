from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MaxValueValidator, MinValueValidator


class Doctor(models.Model):
    name = models.CharField(max_length=200, verbose_name="اسم الطبيب")
    email = models.EmailField(max_length=200, verbose_name="البريد الإلكتروني")
    phone = models.CharField(max_length=200, verbose_name="رقم الهاتف")
    image = models.ImageField(upload_to='doctors/', null=True, blank=True, verbose_name="الصورة")
    specialization = models.CharField(max_length=200, verbose_name="التخصص")
    rate = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)], 
     verbose_name="التقييم") 
    address = models.CharField(max_length=200, verbose_name="العنوان")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخر تحديث")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "طبيب"
        verbose_name_plural = "الأطباء"

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="حساب المستخدم")
    name = models.CharField(max_length=200, verbose_name="اسم المريض")
    email = models.EmailField(max_length=200, verbose_name="البريد الإلكتروني")
    phone = models.CharField(max_length=200, verbose_name="رقم الهاتف")
    address = models.CharField(max_length=200, verbose_name="العنوان")
    age = models.IntegerField(verbose_name="العمر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ النسجيل")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخر تحديث")

    doctor = models.ForeignKey(
        Doctor, 
        on_delete=models.CASCADE, 
        related_name="patients", 
        verbose_name="الطبيب المشرف"
    )
    diagnosis = models.TextField(verbose_name="التشخيص")
    admission_date = models.DateField(verbose_name="تاريخ التسجيل",null=True,blank=True,)
    discharge_date = models.DateField(null=True, blank=True, verbose_name="الموعد المحدد ")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "مريض"
        verbose_name_plural = "المرضى"
