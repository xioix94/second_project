from django.urls import path
from . import views

urlpatterns = [
    path('', views.board),
    path('single/', views.single),
    path('write/',views.board_write),
]
