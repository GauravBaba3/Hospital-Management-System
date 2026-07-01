from django.db import models
from learnapp.models import UserDetails
from doctors.models import DoctorsDetails, Treatments

# Create your models here.
class Discharge(models.Model):
    room_type_choices = [
        ('COMMON WARD', 'common ward'),
        ('SEMI-PRIVATE', 'semi-private'),
        ('PRIVATE AC', 'private ac'),
        ('PRIVATE NON-AC', 'private non-ac'),
        ('DELUXE', 'deluxe'),
    ]

    Patient_name = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    doctor_name = models.ForeignKey(DoctorsDetails, on_delete=models.CASCADE)
    treatment_name = models.ForeignKey(Treatments, on_delete=models.CASCADE)
    discription = models.TextField(max_length=500)
    date_of_addm = models.DateField()
    date_of_discharge = models.DateField()
    room_type = models.CharField(max_length=100, choices=room_type_choices)
    food_required = models.BooleanField()
    total_days = models.PositiveIntegerField()

    def __str__(self):
        return str(self.Patient_name)
    
    