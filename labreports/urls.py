from django.urls import path
from labreports import views

urlpatterns = [
    path('', views.labtech, name='labtech'),
    path('labtest/', views.labtest, name='labtest'),
    path('labtechreg/', views.labtechreg, name='labtechreg'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
