from django.urls import path
from . import views

urlpatterns = [
    path('404/', views.page_404),
    path('blog_single/', views.blog_single),
    path('blog/', views.blog),
    path('contact/', views.contact),
    path('icons/', views.icons),
    path('', views.index),
    path('login/', views.login),
    path('login_form/', views.login_form),
    path('product_single/', views.product_single),
    path('product/', views.product),
    path('profile/', views.profile),
    path('to_members/', views.to_members_form),
    path('userpage/', views.userpage),
    path('register/', views.register),
    path('recommand/', views.recommand),
    path('recommand_result/', views.recommand_result),
    path('userpage/modify', views.comment_modify),
]
