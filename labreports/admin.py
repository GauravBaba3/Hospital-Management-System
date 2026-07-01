from django.contrib import admin 
from labreports.models import LabTechnician, LabTests

# Register your models here.
admin.site.register(LabTechnician)
admin.site.register(LabTests)