from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def page_404(request):
    return render(request, 'app/404.html')

def blog_single(request):
    return render(request, 'app/blog_single.html')

def blog(request):
    return render(request, 'app/blog.html')

def contact(request):
    return render(request, 'app/contact.html')

def icons(request):
    return render(request, 'app/icons.html')

def index(request):
    return render(request, 'app/index.html')

def login_check(request):
    return render(request, 'app/login_check.html')

def login_form(request):
    return render(request, 'app/login_form.html')

def product_single(request):
    return render(request, 'app/product_single.html')

def product(request):
    return render(request, 'app/product.html')

def profile_form(request):
    return render(request, 'app/profile_form.html')

def to_members_form(request):
    return render(request, 'app/to_members.html')


def userpage(request):
    return render(request, 'app/userpage.html')