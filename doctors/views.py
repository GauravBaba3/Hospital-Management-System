from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from doctors.models import DoctorsDetails
from doctors.models import Treatments, Appointment
from doctors.forms import AppointmentForm
from labreports.models import LabTechnician

BOOKING_SESSION_KEY = 'appointment_booking_confirmation'


def home(request):
    if request.user.is_authenticated:
        labtech = LabTechnician.objects.filter(user=request.user).exists()
    else:
        labtech = False
    return render(request, 'doctors/home.html', {'labtech': labtech})


def alldoctors(request):
    alldoc = DoctorsDetails.objects.all()
    return render(request, 'doctors/alldoctors.html', {'alldoc': alldoc})


def doctorprofile(request, id):
    doc = DoctorsDetails.objects.get(id=id)
    return render(request, 'doctors/doctorprofile.html', {'doc': doc})


def treatment(request):
    treatments = Treatments.objects.all()
    unique_treatments = {}
    for t in treatments:
        if t.treatment_name not in unique_treatments:
            unique_treatments[t.treatment_name] = t
    treat1 = unique_treatments.values()
    return render(request, 'treatment/treatment.html', {'treat1': treat1})


def doctorslist(request, treatment_name):
    doclists = Treatments.objects.filter(treatment_name=treatment_name)
    return render(request, 'treatment/doctorslist.html', {'doclists': doclists})


def appointment(request, id):
    doctor = get_object_or_404(DoctorsDetails, id=id)
    treatments = Treatments.objects.filter(doctorname=doctor)
    default_treatment = treatments.first()

    booked = None
    status = False

    if request.GET.get('booked') == '1':
        payload = request.session.pop(BOOKING_SESSION_KEY, None)
        if isinstance(payload, dict) and payload.get('doctor_id') == doctor.id:
            try:
                booked = Appointment.objects.select_related(
                    'doctor',
                    'treatment',
                ).get(pk=int(payload['booking_id']), doctor=doctor)
                status = True
            except (Appointment.DoesNotExist, ValueError, KeyError, TypeError):
                booked = None
                status = False

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        form.fields['treatment'].queryset = treatments
        if form.is_valid():
            obj = form.save()
            request.session[BOOKING_SESSION_KEY] = {
                'booking_id': obj.pk,
                'doctor_id': doctor.id,
            }
            url = f"{reverse('appointment', kwargs={'id': id})}?booked=1"
            return redirect(url)
    else:
        form = AppointmentForm(initial={
            'doctor': doctor,
            'treatment': default_treatment,
        })
        form.fields['treatment'].queryset = treatments

    return render(request, 'doctors/appointment.html', {
        'appointment_form': form,
        'doctor': doctor,
        'status': status,
        'booked': booked,
    })
