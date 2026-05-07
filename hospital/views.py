from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Doctor, Patient, Admin, Appointment, Prescription
import json
import random
import string


# =============================================
# HELPER FUNCTIONS
# =============================================

def make_id():
    chars = string.ascii_lowercase + string.digits
    return "X" + "".join(random.choices(chars, k=8))


# =============================================
# MAIN PAGE — HTML yuboradi
# =============================================

def index(request):
    return render(request, 'index.html')


# =============================================
# AUTH API
# =============================================

@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    data     = json.loads(request.body)
    name     = data.get("name", "").strip()
    password = data.get("password", "").strip()

    if not name or not password:
        return JsonResponse({
            "success": False,
            "message": "Please fill all fields!"
        })

    # Admin tekshirish
    try:
        admin = Admin.objects.get(name=name)
        if admin.check_password(password):
            return JsonResponse({
                "success": True,
                "user": {
                    "id":   str(admin.id),
                    "name": admin.name,
                    "role": "admin"
                }
            })
    except Admin.DoesNotExist:
        pass

    # Doctor tekshirish
    try:
        doctor = Doctor.objects.get(name=name)
        if doctor.check_password(password):
            return JsonResponse({
                "success": True,
                "user": {
                    "id":   str(doctor.id),
                    "name": doctor.name,
                    "role": "doctor",
                    "spec": doctor.spec
                }
            })
    except Doctor.DoesNotExist:
        pass

    # Patient tekshirish
    try:
        patient = Patient.objects.get(name=name)
        if patient.check_password(password):
            return JsonResponse({
                "success": True,
                "user": {
                    "id":   str(patient.id),
                    "name": patient.name,
                    "role": "patient"
                }
            })
    except Patient.DoesNotExist:
        pass

    return JsonResponse({
        "success": False,
        "message": "Wrong name or password!"
    })


@csrf_exempt
@require_http_methods(["POST"])
def logout(request):
    return JsonResponse({"success": True})


# =============================================
# PATIENTS API
# =============================================

def get_patients(request):
    patients = Patient.objects.all()
    data = []
    for p in patients:
        data.append({
            "id":        str(p.id),
            "name":      p.name,
            "age":       p.age,
            "blood":     p.blood,
            "diagnosis": p.diagnosis,
            "status":    p.status,
            "phone":     p.phone
        })
    return JsonResponse({"success": True, "data": data})


@csrf_exempt
def add_patient(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name", "").strip()

        if not name:
            return JsonResponse({
                "success": False,
                "message": "Name required!"
            })

        patient = Patient.objects.create(
            name      = name,
            password  = name.split()[0].lower() + "123",
            role      = "patient",
            age       = int(data.get("age") or 0),
            blood     = data.get("blood", "A+"),
            diagnosis = data.get("diagnosis", ""),
            status    = "Stable",
            phone     = data.get("phone", "")
        )

        return JsonResponse({
            "success": True,
            "message": name + " added!",
            "data": {
                "id":   str(patient.id),
                "name": patient.name
            }
        })


@csrf_exempt
def update_patient(request, pid):
    if request.method == "PUT":
        data    = json.loads(request.body)
        try:
            patient = Patient.objects.get(id=pid)
            patient.status    = data.get(
                "status", patient.status)
            patient.diagnosis = data.get(
                "diagnosis", patient.diagnosis)
            patient.phone     = data.get(
                "phone", patient.phone)
            patient.save()
            return JsonResponse({
                "success": True,
                "message": "Updated!"
            })
        except Patient.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Not found!"
            })


@csrf_exempt
def delete_patient(request, pid):
    if request.method == "DELETE":
        try:
            Patient.objects.get(id=pid).delete()
            return JsonResponse({
                "success": True,
                "message": "Deleted!"
            })
        except Patient.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Not found!"
            })


# =============================================
# DOCTORS API
# =============================================

def get_doctors(request):
    doctors = Doctor.objects.all()
    data = []
    for d in doctors:
        data.append({
            "id":        str(d.id),
            "name":      d.name,
            "spec":      d.spec,
            "exp":       d.exp,
            "rating":    d.rating,
            "available": d.available
        })
    return JsonResponse({"success": True, "data": data})


# =============================================
# APPOINTMENTS API
# =============================================

def get_appointments(request):
    apts = Appointment.objects.all()
    data = []
    for a in apts:
        data.append({
            "id":       str(a.id),
            "patient":  a.patient_name,
            "doctor":   a.doctor_name,
            "date":     str(a.date),
            "time":     str(a.time)[:5],
            "priority": a.priority,
            "status":   a.status
        })
    return JsonResponse({"success": True, "data": data})


@csrf_exempt
def add_appointment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        apt  = Appointment.objects.create(
            patient_name = data.get("patient", ""),
            doctor_name  = data.get("doctor", ""),
            date         = data.get("date", ""),
            time         = data.get("time", "09:00"),
            priority     = data.get("priority", "Normal"),
            status       = "Pending"
        )
        return JsonResponse({
            "success": True,
            "message": "Scheduled!"
        })


@csrf_exempt
def update_appointment(request, aid):
    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            apt        = Appointment.objects.get(id=aid)
            apt.status = data.get("status", apt.status)
            apt.save()
            return JsonResponse({
                "success": True,
                "message": "Updated!"
            })
        except Appointment.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Not found!"
            })


# =============================================
# PRESCRIPTIONS API
# =============================================

def get_prescriptions(request):
    rxs  = Prescription.objects.all()
    data = []
    for rx in rxs:
        data.append({
            "id":       str(rx.id),
            "patient":  rx.patient_name,
            "doctor":   rx.doctor_name,
            "drug":     rx.drug,
            "dosage":   rx.dosage,
            "duration": rx.duration,
            "status":   rx.status
        })
    return JsonResponse({"success": True, "data": data})


@csrf_exempt
def add_prescription(request):
    if request.method == "POST":
        data = json.loads(request.body)
        drug = data.get("drug", "").strip()

        if not drug:
            return JsonResponse({
                "success": False,
                "message": "Drug name required!"
            })

        rx = Prescription.objects.create(
            patient_name = data.get("patient", ""),
            doctor_name  = data.get("doctor", ""),
            drug         = drug,
            dosage       = data.get("dosage", ""),
            duration     = data.get("duration", ""),
            status       = "Active"
        )
        return JsonResponse({
            "success": True,
            "message": "Issued!"
        })


@csrf_exempt
def update_prescription(request, rid):
    if request.method == "PUT":
        try:
            rx        = Prescription.objects.get(id=rid)
            rx.status = "Revoked"
            rx.save()
            return JsonResponse({
                "success": True,
                "message": "Revoked!"
            })
        except Prescription.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Not found!"
            })


# =============================================
# REPORTS API
# =============================================

def get_reports(request):
    patients = Patient.objects.all()
    return JsonResponse({
        "success": True,
        "data": {
            "total_patients":       patients.count(),
            "stable_patients":      patients.filter(
                                        status="Stable"
                                    ).count(),
            "critical_patients":    patients.filter(
                                        status="Critical"
                                    ).count(),
            "total_doctors":        Doctor.objects.count(),
            "total_appointments":   Appointment.objects.count(),
            "pending_appointments": Appointment.objects.filter(
                                        status="Pending"
                                    ).count(),
            "active_prescriptions": Prescription.objects.filter(
                                        status="Active"
                                    ).count(),
        }
    })