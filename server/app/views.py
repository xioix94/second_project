from django.db.models.query import QuerySet
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.contrib import messages
from django import forms
from django.core.paginator import Paginator



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


# 추천 페이지에 맥주 데이터 가져오기 (16개)
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
    category = request.GET.get('category')

    products = Product.objects.none()
    if category:
        category_id = Category.objects.get(name=category)
        products = Product.objects.filter(category_id=category_id)
    else:
        category = "all"
        products = Product.objects.all()

    return render(request, 'app/product.html', {
        'product_list': products,
        'category': category}
        )


def profile(request):
    if request.method == 'GET':
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
    else:
        nickname = request.POST['nickname']
        password = request.POST['password']

        try:
            email = request.session.get('email')
            user = User.objects.get(email=email)
            user.alias = nickname
            user.password = password
            user.save()
            result = "Success"
            messages = "Profile change succeeded."
        except:
            result = "Fail"
            messages = "Profile change failed."
            # return render(request, 'app/login.html', {'messages' : messages})

        return JsonResponse({'result': result, 'messages': messages})


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
            request.session['alias'] = member.alias
            return render(request, 'app/index.html')



def comment_modify(request):


    if request.method == "POST":
        form = userpage(request.POST, instance=user_comments)

        if form.is_valid():
            user_comments = form.save(commit=False)
            user_comments.save()
            messages.success(request,'수정되었습니다')
            return redirect('app:userpage', user_id = user.id)

    elif request.method == "GET":
        # 수정페이지 보여주는 역할
        comment_id = request.GET.get('comment_id')
        user_comment = Product_Comment.objects.get(id=comment_id)

        return render(request, 'app/freewrite.html')

    else:
        pass





def logout(request):
    request.session.clear()
    return redirect('/')