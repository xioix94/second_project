from django.urls import path
from . import views

urlpatterns = [
    path('email_valid_duplicate/', views.email_valid_duplicate),
    path('alias_valid/', views.alias_valid),
    path('register/', views.register),
    path('login/', views.login),
]
