from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from labreports.models import LabTechnician, LabTests
from labreports.forms import LabTechnicianRegForm
import random
from django.core.paginator import Paginator

# Create your views here.
def labtech(request):
    tech_details = LabTechnician.objects.all()
    return render(request, 'labreports/labtech.html', {'tech_details':tech_details})



def labtechreg(request):
    if request.method == 'POST':
        form1 = LabTechnicianRegForm(request.POST)
        if form1.is_valid():
            form1.save()
            return redirect('login')
    else:
        form1 = LabTechnicianRegForm()

    return render(request, 'labreports/labtechreg.html', {'form1':form1})




@login_required(login_url='login')
def labtest(request):
    lab_tech = LabTechnician.objects.filter(user=request.user).first()
    if lab_tech is None:
        return render(
            request,
            'labreports/labtest.html',
            {'data': [], 'no_lab_profile': True},
        )

    tech_details = LabTests.objects.filter(patient_name__user=request.user)
    data = []
    for obj in tech_details:
        data.append({
            'test': obj,
            'lab_tech': lab_tech,
            'rand_num': random.randint(200, 1000),
        })

    return render(request, 'labreports/labtest.html', {'data': data})



def dashboard(request):
    lab_test_list = LabTests.objects.all().order_by('-id')
    paginator = Paginator(lab_test_list, 10)
    page_number = request.GET.get('pg')
    records = paginator.get_page(page_number)
    context = {
        'records': records
    }
    return render(request, 'labreports/dashboard.html', context)