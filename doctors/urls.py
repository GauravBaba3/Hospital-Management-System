from django.urls import path
from doctors import views

urlpatterns = [
    path("", views.home, name='doctorshome'),
    path("alldoctors", views.alldoctors, name='alldoctors'),
    path('doctorprofile/<int:id>/', views.doctorprofile, name='doctorprofile'),
    path("treatment/", views.treatment, name='treatment'),
    path("doctorslist/<str:treatment_name>/", views.doctorslist, name='doctorslist'),
    path("appointment/<int:id>/", views.appointment, name='appointment'),
]
