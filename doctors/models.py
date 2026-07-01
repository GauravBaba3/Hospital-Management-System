from django.db import models
from datetime import date

# choices
SPECIALITY_CHOICES = [
    ("general medicine", "GENERAL MEDICINE"),
    ("cardiologist", "CARDIOLOGIST"),
    ("ent", "ENT"),
    ("orthopedic", "ORTHOPEDIC"),
    ("eye specialist", "EYE SPECIALIST"),
    ("dentist", "DENTIST"),
    ("others", "OTHERS"),
]


class DoctorsDetails(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    specs = models.CharField(max_length=100, choices=SPECIALITY_CHOICES)
    phone = models.PositiveBigIntegerField()
    mail = models.EmailField(max_length=100)
    loc = models.CharField(max_length=100)
    about = models.CharField(max_length=1000)
    docpic = models.ImageField(upload_to='doctorimg/', null=True, blank=True)

    def __str__(self):
        return self.name


class Treatments(models.Model):
    treatment_name = models.CharField(max_length=100)
    catogery = models.CharField(max_length=100, choices=SPECIALITY_CHOICES)
    doctorname = models.ForeignKey(DoctorsDetails, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.treatment_name
    

class Appointment(models.Model):
    TIME_SLOTS = [
    ('09:00:00', '09:00 AM'),
    ('10:00:00', '10:00 AM'),
    ('11:00:00', '11:00 AM'),
    ]
    doctor = models.ForeignKey(DoctorsDetails, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatments, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    fee = models.PositiveIntegerField(default=500)
    patient_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    time = models.CharField(choices=TIME_SLOTS)
    problem = models.TextField()

    def __str__(self):
        return str(self.patient_name)
