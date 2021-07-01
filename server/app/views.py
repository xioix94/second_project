from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Product_Comment, User, Product
import random

# Create your views here.
def page_404(request):
    return render(request, 'app/404.html')

def blog_single(request):
    return render(request, 'app/blog_single.html')

def blog(request):
    p_comments = Product_Comment.objects.all().select_related('product').select_related('user')

    return render(request, 'app/blog.html', {
        'p_comments': p_comments})

def contact(request):
    return render(request, 'app/contact.html')
    

def icons(request):
    return render(request, 'app/icons.html')

def index(request):
    return render(request, 'app/index.html')

# 추천 페이지에 제품 데이터 가져오기 (16개)
def recommand(request):
    products = Product.objects.order_by('?')[:16]
        
    return render(request, 'app/recommand.html', {
        'products': products
    })

# 추천 페이지 결과를 이용 -> 머신러닝(클러스터링) -> 결과값과 동일한 군집의 제품 데이터 가져오기 (16개) 
def recommand_result(request):
    # 머신러닝 나온 군집 안의 제품으로 줘야 함                     (수정 필요)
    products = Product.objects.order_by('?')[:16]
        
    return render(request, 'app/recommand_result.html', {
        'products': products
    })

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

    
    user_comments = Product_Comment.objects.filter(user_id=user.id).select_related('product')



    return render(request, 'app/userpage.html', {
        'user': user,
        'user_comments': user_comments,
    })

def register(request):
    return render(request, 'app/register.html')

def change_user_info(request):
    return render(request, 'app/change_user_info.html')

def login(request):
    if request.method == 'GET':
        return render(request, 'app/login.html', {})
    else:
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            member = User.objects.get(email=email,password=password)
        except:
            messages = "실패"
            return render(request, 'app/login.html', {'messages' : messages})
        else:
            request.session['email'] = email
            return render(request, 'app/index.html')
