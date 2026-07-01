from django.urls import path
from payments import views

urlpatterns = [
    path('', views.Discharges, name='discharge'),
    path('finalbill/<int:id>/', views.finalbill, name='finalbill'),
    path('pay/<int:id>/', views.payment_checkout, name='payment_checkout'),
    path('payment-success/<int:id>/', views.payment_success, name='payment_success'),
]
