from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Product_Comment, User, Product

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
    product_list = Product.objects.all()
    return render(request, 'app/product.html', {'product_list': product_list})

def profile_form(request):
    # 현재 로그인한 user 정보를 DB에서 가져옴
    try:
        email = request.GET.get('email')
        
        user = User.objects.get(email=email)

        nickname = user.alias
        password = user.password

        return render(request, 'app/profile_form.html', {
            'nickname': nickname,
            'password': password,
        })
    except:
        return render(request, 'app/login.html', {})


def to_members_form(request):
    return render(request, 'app/to_members.html')


def userpage(request):
    email = request.GET.get('email')
    
    user = User.objects.get(email=email)
    
    user_comments = Product_Comment.objects.filter(user_id=user.id)


    return render(request, 'app/userpage.html', {
        'user': user,
        'user_comments': user_comments,
    })

def register(request):
    return render(request, 'app/register.html')

def change_user_info(request):
    return render(request, 'app/change_user_info.html')