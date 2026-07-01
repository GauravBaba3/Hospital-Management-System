from django import forms
from doctors.models import DoctorsDetails
from doctors.models import Treatments, Appointment

class DoctorsForms(forms.ModelForm):
    class Meta:
        model = DoctorsDetails
        fields = '__all__'


class TreatmentsForm(forms.ModelForm):
    class Meta:
        model = Treatments
        fields = '__all__'


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'treatment', 'date', 'fee', 'patient_name', 'phone', 'time', 'problem']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'problem': forms.Textarea(attrs={'rows': 4,'cols': 40}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fee'].disabled = True
