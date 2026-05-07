from django.db import models


# =============================================
# OOP — CLASS va INHERITANCE
# =============================================

# BASE CLASS
class User(models.Model):
    """
    Barcha foydalanuvchilar uchun asosiy class
    ENCAPSULATION — ma'lumotlar himoyalangan
    """
    ROLE_CHOICES = [
        ('admin',   'Admin'),
        ('doctor',  'Doctor'),
        ('patient', 'Patient'),
    ]

    name     = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    role     = models.CharField(
                   max_length=20,
                   choices=ROLE_CHOICES
               )

    class Meta:
        abstract = True  # ABSTRACTION — to'g'ridan yaratib bo'lmaydi

    def check_password(self, input_pass):
        """ENCAPSULATION — passwordni faqat shu orqali tekshirish"""
        return self.password == input_pass

    def __str__(self):
        return self.name


# DERIVED CLASS — INHERITANCE
class Doctor(User):
    """Doctor class — User dan meros olgan"""
    SPECIALIZATIONS = [
        ('Cardiologist',    'Cardiologist'),
        ('Neurologist',     'Neurologist'),
        ('Endocrinologist', 'Endocrinologist'),
        ('Surgeon',         'Surgeon'),
        ('Pediatrician',    'Pediatrician'),
    ]

    spec      = models.CharField(
                    max_length=100,
                    choices=SPECIALIZATIONS
                )
    exp       = models.IntegerField(default=0)
    rating    = models.FloatField(default=5.0)
    available = models.BooleanField(default=True)
    email     = models.EmailField(blank=True)
    phone     = models.CharField(max_length=20, blank=True)

    # POLYMORPHISM — get_dashboard boshqacha ishlaydi
    def get_dashboard(self):
        return {
            "type":    "doctor",
            "name":    self.name,
            "spec":    self.spec,
            "rating":  self.rating,
            "message": "My patients and appointments"
        }

    # ENCAPSULATION — faqat Doctor qila oladi
    def issue_prescription(self, patient_name, drug):
        return (self.name + " prescribed " +
                drug + " to " + patient_name)

    class Meta:
        db_table = 'doctors'

    def __str__(self):
        return "Dr. " + self.name


# DERIVED CLASS — INHERITANCE
class Patient(User):
    """Patient class — User dan meros olgan"""
    STATUS_CHOICES = [
        ('Stable',     'Stable'),
        ('Monitoring', 'Monitoring'),
        ('Critical',   'Critical'),
        ('Checkup',    'Checkup'),
    ]

    BLOOD_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+','AB+'),('AB-','AB-'),
    ]

    age       = models.IntegerField(default=0)
    blood     = models.CharField(
                    max_length=5,
                    choices=BLOOD_CHOICES
                )
    diagnosis = models.CharField(max_length=200, blank=True)
    status    = models.CharField(
                    max_length=20,
                    choices=STATUS_CHOICES,
                    default='Stable'
                )
    phone     = models.CharField(max_length=20, blank=True)
    email     = models.EmailField(blank=True)

    # POLYMORPHISM — get_dashboard boshqacha ishlaydi
    def get_dashboard(self):
        return {
            "type":      "patient",
            "name":      self.name,
            "diagnosis": self.diagnosis,
            "status":    self.status,
            "message":   "My personal health records"
        }

    # ENCAPSULATION — faqat Patient qila oladi
    def book_appointment(self, doctor_name, date):
        return (self.name + " booked with Dr." +
                doctor_name + " on " + date)

    class Meta:
        db_table = 'patients'

    def __str__(self):
        return self.name


# DERIVED CLASS — INHERITANCE
class Admin(User):
    """Admin class — User dan meros olgan"""

    # POLYMORPHISM — get_dashboard boshqacha ishlaydi
    def get_dashboard(self):
        return {
            "type":    "admin",
            "name":    self.name,
            "message": "Full hospital control"
        }

    class Meta:
        db_table = 'admins'

    def __str__(self):
        return "Admin: " + self.name


# APPOINTMENT MODEL
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending',   'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    PRIORITY_CHOICES = [
        ('Normal', 'Normal'),
        ('High',   'High'),
        ('Urgent', 'Urgent'),
    ]

    patient_name = models.CharField(max_length=100)
    doctor_name  = models.CharField(max_length=100)
    date         = models.DateField()
    time         = models.TimeField()
    priority     = models.CharField(
                       max_length=20,
                       choices=PRIORITY_CHOICES,
                       default='Normal'
                   )
    status       = models.CharField(
                       max_length=20,
                       choices=STATUS_CHOICES,
                       default='Pending'
                   )

    class Meta:
        db_table = 'appointments'

    def __str__(self):
        return (self.patient_name + " → Dr." +
                self.doctor_name)


# PRESCRIPTION MODEL
class Prescription(models.Model):
    STATUS_CHOICES = [
        ('Active',  'Active'),
        ('Revoked', 'Revoked'),
    ]

    patient_name = models.CharField(max_length=100)
    doctor_name  = models.CharField(max_length=100)
    drug         = models.CharField(max_length=200)
    dosage       = models.CharField(max_length=100)
    duration     = models.CharField(max_length=100)
    status       = models.CharField(
                       max_length=20,
                       choices=STATUS_CHOICES,
                       default='Active'
                   )

    class Meta:
        db_table = 'prescriptions'

    def __str__(self):
        return self.drug + " → " + self.patient_name