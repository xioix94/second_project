from django.urls import path
from . import views

urlpatterns = [
    path('', views.board),
    path('single/', views.single),
    path('edit/', views.edit_comment),
    path('board_edit/', views.board_edit),
    path('write/',views.board_write),
    path('single/<int:pk>/delete/', views.board_delete),
]
