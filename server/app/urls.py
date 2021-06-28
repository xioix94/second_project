from django.urls import path
from . import views

urlpatterns = [
    path('404/', views.page_404),
    path('blog_single/', views.blog_single),
    path('blog/', views.blog),
    path('contact/', views.contact),
    path('icons/', views.icons),
    path('', views.index),
    path('login_check/', views.login_check),
    path('login_form/', views.login_form),
    path('product_single/', views.product_single),
    path('product/', views.product),
]
