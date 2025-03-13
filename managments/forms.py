from django import forms
from django.contrib.auth.models import User
from .models import Patient,Appointment

class PatientRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=False,  # No need for username if user is logged in
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "اسم المستخدم"})
    )
    password = forms.CharField(
        required=False,  # No need for password if user is logged in
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "كلمة المرور"})
    )

    class Meta:
        model = Patient
        fields = ["name", "email", "phone", "address", "age", "doctor", "diagnosis"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "أدخل اسمك"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "أدخل بريدك الإلكتروني"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "أدخل رقم هاتفك"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "أدخل عنوانك"}),
            "age": forms.NumberInput(attrs={"class": "form-control", "placeholder": "أدخل عمرك"}),
            "doctor": forms.Select(attrs={"class": "form-select"}),  # Dropdown
            "diagnosis": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "أدخل التشخيص"}),
        }

    def save(self, request, commit=True):
        if request.user.is_authenticated:
            patient, created = Patient.objects.get_or_create(user=request.user)
        else:
            user = User.objects.create_user(
                username=self.cleaned_data["username"],
                password=self.cleaned_data["password"]
            )
            patient = super().save(commit=False)
            patient.user = user  # Assign new user to patient

        if commit:
            patient.save()
        return patient
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["date", "reason"]
        widgets = {
            "date": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "reason": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "أدخل سبب الزيارة"}),
        }
        
