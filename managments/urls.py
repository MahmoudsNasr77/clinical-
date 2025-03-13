app_name="managments"
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('doctor', views.doctor, name='doctor'),
    path('patient', views.patient_dashboard, name='patient'),
    path('register',views.register_patient,name="painetSignup"),
    path("login/", views.PatientLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="managments:login"), name="logout"),
        path("update-discharge/<int:patient_id>/", views.update_discharge_date, name="update_discharge_date"),
        path("book_appointment", views.book_appointment, name="book_appointment"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)