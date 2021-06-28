from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def page_404(request):
    return render(request, 'app/404.html')


def index(request):
    return render(request, 'app/index.html')
