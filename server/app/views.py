from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
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


def login_form(request):
    return render(request, 'app/login_form.html')

def product_single(request):
    try:
        product_id = request.GET.get('p_id')
        
        product = Product.objects.get(id=product_id)
        product_comment_list = Product_Comment.objects.filter(product_id=product.id).select_related('user')

        p_name = product.name
        p_image = product.image
        p_alcohol = product.alcohol
        p_category_id = product.category_id

        dict = {'bold': 0, 'sparkling': 0,'sweet': 0,'tannic': 0,'acidic': 0,'bold': 0, 'score': 0}
        for p in product_comment_list:
            dict['bold'] += p.bold
            dict['sparkling'] += p.sparkling
            dict['sweet'] += p.sweet
            dict['tannic'] += p.tannic
            dict['acidic'] += p.acidic
            dict['score'] += p.score

        dict['bold'] = (dict['bold'] / len(product_comment_list)) * 100
        dict['sparkling'] = (dict['sparkling'] / len(product_comment_list)) * 100
        dict['sweet'] = (dict['sweet'] / len(product_comment_list))  * 100
        dict['tannic'] = (dict['tannic'] / len(product_comment_list))  * 100
        dict['acidic'] = (dict['acidic'] / len(product_comment_list))  * 100
        dict['score'] = (dict['score'] / len(product_comment_list)) * 20 # 5점만점을 퍼센트로 변환

        return render(request, 'app/product_single.html', {
            'name': p_name,
            'image': p_image,
            'alcohol': p_alcohol,
            'category_id': p_category_id,
            'taste': dict,
            'product_comment_list': product_comment_list,
        })
    except:
        return render(request, 'app/product.html')

def product(request):
    product_list = Product.objects.all()
    return render(request, 'app/product.html', {'product_list': product_list})

def profile_form(request):
    # 현재 로그인한 user 정보를 DB에서 가져옴
    try:
        email = request.session.get('email')
        user = User.objects.get(email=email)

        nickname = user.alias
        password = user.password

        return render(request, 'app/profile_form.html', {
            'nickname': nickname,
            'password': password,
        })
    except:
        return render(request, 'app/login.html', {})

def save_profile(request):
    if request.method == 'GET':
        return render(request, 'app/profile_form.html', {})
    else:
        nickname = request.POST['nickname']
        password = request.POST['password']
        
        try:
            email = request.session.get('email')
            user = User.objects.get(email=email)
            user.alias = nickname
            user.password = password
            user.save()
            
            return redirect('app/profile_form.html')
        except:
            messages = "실패"
            return render(request, 'app/login.html', {'messages' : messages})

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
