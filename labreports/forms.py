from django import forms
from labreports.models import LabTechnician, LabTests
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from labreports.models import LabTechnician

# class LabTechnicianRegForm(UserCreationForm):
#     emp_id = forms.CharField(max_length=20)
#     qualification = forms.CharField(max_length=100)
#     years_of_experiance = forms.IntegerField()
#     address = forms.CharField(max_length=100)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

#     def save(self, comm):
#         user = super().save(commit=False)
#         user.save()

#         self.emp_id = self.cleaned_data['emp_id']
#         self.qualification = self.cleaned_data['qualification']
#         self.years_of_experiance = self.cleaned_data['years_of_experiance']
#         self.address = self.cleaned_data['address']

#         LabTechnician.objects.create(
#             user = user,
#             emp_id = self.emp_id,
#             qualification = self.qualification,
#             years_of_experiance = self.years_of_experiance,
#             address = self.address
#         )
#         LabTechnician.save()
#         return LabTechnician



class LabTechnicianRegForm(UserCreationForm):
    emp_id = forms.CharField(max_length=20)
    qualification = forms.CharField(max_length=100)
    years_of_experiance = forms.IntegerField()
    address = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)

        LabTechnician.objects.create(
            user=user,
            emp_id=self.cleaned_data['emp_id'],
            qualification=self.cleaned_data['qualification'],
            years_of_experiance=self.cleaned_data['years_of_experiance'],
            address=self.cleaned_data['address']
        )

        return user



class LabTestsForms(forms.ModelForm):
    class Meta:
        model = LabTests
        fields = '__all__'