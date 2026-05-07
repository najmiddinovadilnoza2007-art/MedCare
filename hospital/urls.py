from django.urls import path
from . import views

urlpatterns = [

    # Main page
    path('', views.index, name='index'),

    # Auth
    path('api/login',  views.login,  name='login'),
    path('api/logout', views.logout, name='logout'),

    # Patients
    path('api/patients',
         views.get_patients,  name='get_patients'),
    path('api/patients/add',
         views.add_patient,   name='add_patient'),
    path('api/patients/<int:pid>/update',
         views.update_patient, name='update_patient'),
    path('api/patients/<int:pid>/delete',
         views.delete_patient, name='delete_patient'),

    # Doctors
    path('api/doctors',
         views.get_doctors, name='get_doctors'),

    # Appointments
    path('api/appointments',
         views.get_appointments, name='get_appointments'),
    path('api/appointments/add',
         views.add_appointment,  name='add_appointment'),
    path('api/appointments/<int:aid>/update',
         views.update_appointment,
         name='update_appointment'),

    # Prescriptions
    path('api/prescriptions',
         views.get_prescriptions, name='get_prescriptions'),
    path('api/prescriptions/add',
         views.add_prescription,  name='add_prescription'),
    path('api/prescriptions/<int:rid>/update',
         views.update_prescription,
         name='update_prescription'),

    # Reports
    path('api/reports',
         views.get_reports, name='get_reports'),
]