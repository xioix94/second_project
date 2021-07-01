from django.urls import path
from . import views

urlpatterns = [
    path('email_valid/', views.email_valid),
    path('email_duplicate/', views.email_duplicate),
    path('login/', views.login),
    ]
