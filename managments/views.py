from django.contrib import messages
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse_lazy
from .models import Doctor, Patient
from .forms import PatientRegistrationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

# Create your views here.
def index(request):
    doctor=Doctor.objects.all()[:5]
    return render(request, 'index.html', {'doctors': doctor})
def doctor(request):
    doctor=Doctor.objects.all()
    return render(request, 'doctor/doctor.html', {'doctors': doctor})

@login_required(login_url='managments:login')  # Redirects to the login page if not authenticated
def patient_dashboard(request):
    if request.user.is_superuser:
        patients = Patient.objects.all()  # Superuser sees all patients
    else:
        patients = Patient.objects.filter(user=request.user)  # Normal user sees only their info

    return render(request, "patient/patient_dashboard.html", {"patients": patients})
def register_patient(request):
    if request.method == "POST":
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            patient = form.save()
            login(request, patient.user)  # Log in user after registration
            return redirect("managments:patient")
    else:
        form = PatientRegistrationForm()
    
    return render(request, "register.html", {"form": form})

class PatientLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True  # Redirect logged-in users to a different page
    next_page = reverse_lazy('managments:index')  # Change to the correct view name
    
@login_required
def update_discharge_date(request, patient_id):
    if not request.user.is_superuser:
        return redirect("managments:patient")  # Redirect unauthorized users

    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == "POST":
        discharge_date = request.POST.get("discharge_date")
        if discharge_date:
            patient.discharge_date = discharge_date
            patient.save()
            messages.success(request, "تم تحديث تاريخ الخروج بنجاح.")
        else:
            messages.error(request, "الرجاء إدخال تاريخ صالح.")

    return redirect("managments:patient")  # Redirect back to the patient list