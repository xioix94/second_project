from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('email_check/', views.email_check),
    path('password_valid/', views.password_valid),
    path('alias_valid/', views.alias_valid),
]
