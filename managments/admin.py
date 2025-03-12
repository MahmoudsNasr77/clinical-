from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Doctor, Patient

# تخصيص إعدادات لوحة التحكم
admin.site.site_header = _("لوحة تحكم العيادة")
admin.site.site_title = _("إدارة العيادة")
admin.site.index_title = _("مرحبًا بك في لوحة تحكم العيادة")

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "specialization", "created_at")
    search_fields = ("name", "email", "specialization")
    list_filter = ("specialization", "created_at")
    ordering = ("-created_at",)
    fieldsets = (
        (_("المعلومات الشخصية"), {"fields": ("name", "email", "phone", "image")}),
        (_("التخصص والعنوان"), {"fields": ("specialization", "address")}),
        (_("التواريخ"), {"fields": ("created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at")

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "age", "doctor", "admission_date")
    search_fields = ("name", "email", "doctor__name")
    list_filter = ("doctor", "admission_date")
    ordering = ("-admission_date",)
    fieldsets = (
        (_("المعلومات الشخصية"), {"fields": ("name", "email", "phone", "address", "age")}),
        (_("التشخيص والعلاج"), {"fields": ("doctor", "diagnosis")}),
        (_("التواريخ"), {"fields": ("admission_date", "discharge_date", "created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at")
