from django.http.request import HttpRequest
from django.http.response import HttpResponse
from database.models import Category
from django.shortcuts import render

# Create your views here.
def start(request):
    Category(category_name="맥주").save()
    Category(category_name="와인").save()
    Category(category_name="캌테일").save()
    return HttpResponse('success ')
