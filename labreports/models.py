from django.db import models
from django.contrib.auth.models import User
from doctors.models import DoctorsDetails
from learnapp.models import UserDetails

# Create your models here.

class LabTechnician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    emp_id = models.CharField(max_length=20)
    qualification = models.CharField(max_length=100)
    years_of_experiance = models.IntegerField()
    address = models.CharField(max_length=100)

    def __str__(self):
        return str(self.user)


all_lab_tests = [
    ('CBC', 'cbc'),
    ('LFT', 'lft'),
    ('URINE TOTAL TEST', 'urine total test'),
    ('URINE MICROSCOPIC', 'urine microscopic'),
    ('SERUM ROUTINE', 'serum routine'),
    ('THYROID', 'thyroid')
]

test_result = [
    ('PENDING', 'pending'),
    ('ONGOING', 'ongoing'),
    ('COMPLETED', 'completed'),
]

test_range = [
    ('NILL', 'nill'),
    ('POSITIVE', 'positive'),
    ('NEGETIVE', 'negetive'),
    ('NORMAL', 'normal'),
    ('ABNORMAL', 'abnormal'),
]

class LabTests(models.Model):
    reffered_by = models.ForeignKey(DoctorsDetails, on_delete=models.CASCADE)
    patient_name = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    lab_test = models.CharField(max_length=100, choices=all_lab_tests)
    lab_result = models.CharField(max_length=100, choices=test_result)
    created_at = models.DateTimeField(auto_now_add=True)
    result_range = models.CharField(max_length=100, choices=test_range)
    result_desc = models.TextField()
    test_cost = models.IntegerField()

    def __str__(self):
        return str(self.patient_name)