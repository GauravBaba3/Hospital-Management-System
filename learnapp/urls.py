from django.urls import path
from learnapp import views

urlpatterns = [
    path('', views.registration, name='register'),
    path('login/', views.user_login, name='login'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('logout', views.user_logout, name='logout'),
    path('update-profile/', views.update_user_details, name='update_profile'),
]
