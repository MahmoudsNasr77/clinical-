from django.contrib import messages
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse_lazy
from .models import Doctor, Patient,Appointment
from .forms import PatientRegistrationForm,AppointmentForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
# Create your views here.
def index(request):
    doctor=Doctor.objects.all()[:5]
    return render(request, 'index.html', {'doctor': doctor})
def doctor(request):
    doctor=Doctor.objects.all()
    return render(request, 'doctor/doctor.html', {'doctors': doctor})

@login_required(login_url='managments:login')  # Redirects to the login page if not authenticated
def patient_dashboard(request):
    if request.user.is_superuser:
        patients = Patient.objects.prefetch_related("appointment_set").all()  # Load all patients with their appointments
    else:
        patients = Patient.objects.filter(user=request.user).prefetch_related("appointment_set")

    return render(request, "patient/patient_dashboard.html", {"patients": patients})
def register_patient(request):
    if request.user.is_authenticated:
        patient, created = Patient.objects.get_or_create(user=request.user)

        if request.method == "POST":
            form = PatientRegistrationForm(request.POST, instance=patient)
            if form.is_valid():
                form.save(request)
                return redirect("managments:patient")
        else:
            form = PatientRegistrationForm(instance=patient, initial={"name": request.user.username})  # Autofill

    else:
        if request.method == "POST":
            form = PatientRegistrationForm(request.POST)
            if form.is_valid():
                patient = form.save(request)
                login(request, patient.user)  # Log in new user
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


def appointment(request):
    appointment=Appointment.objects.all()
    return render(request, 'appointment.html', {'appointment': appointment})
@login_required
def book_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)  # Don't save yet
            
            # Ensure the user has a patient profile
            try:
                appointment.patient = request.user.patient  # Assign the patient
                appointment.save()
                return redirect("managments:patient")  # Redirect to dashboard
            except Patient.DoesNotExist:
                form.add_error(None, "يجب أن يكون لديك حساب مريض لحجز موعد.")

    else:
        form = AppointmentForm()

    return render(request, "appointment_form.html", {"form": form})