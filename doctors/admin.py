from django.contrib import admin
from doctors.models import DoctorsDetails,Treatments, Appointment

# Register your models here.
admin.site.register(DoctorsDetails)
admin.site.register(Treatments)
admin.site.register(Appointment)