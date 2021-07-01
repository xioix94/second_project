from django.db.models.query import QuerySet
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Category, Product_Comment, User, Product
from itertools import chain

# Create your views here.
def page_404(request):
    return render(request, 'app/404.html')

def blog_single(request):
    return render(request, 'app/blog_single.html')

def blog(request):
    category = request.GET.get('category')

    p_comments = Product_Comment.objects.none()
    if category:
        category_id = Category.objects.get(name=category)
        products = Product.objects.filter(category_id=category_id)
        for product in products:
            p_comments = p_comments | Product_Comment.objects.select_related().filter(product_id=product.id)
    else:
        p_comments = Product_Comment.objects.select_related()

    return render(request, 'app/blog.html', {
        'p_comments': p_comments,
        'category': category})

def contact(request):
    return render(request, 'app/contact.html')
    

def icons(request):
    return render(request, 'app/icons.html')

def index(request):
    return render(request, 'app/index.html')

def recommand(request):
    return render(request, 'app/recommand.html')


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
