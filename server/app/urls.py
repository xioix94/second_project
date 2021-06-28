from django.urls import path
from . import views

urlpatterns = [
    path('404/', views.page_404),
    path('', views.index),
]
