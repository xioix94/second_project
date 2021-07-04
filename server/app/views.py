from django.db.models.query import QuerySet
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.contrib import messages
from django import forms
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


# Create your views here.
def page_404(request):
    return render(request, 'app/404.html')



def blog_single(request):
    return render(request, 'app/blog_single.html')


#리뷰 모음 페이지
def blog(request):
    # 카테고리 필터
    category = request.GET.get('category')
    if category in ['beer', 'wine', 'cocktail']:
        category = Category.objects.get(name=category)
        products = Product.objects.filter(category_id=category.id)
    else:
        category = 'all'
        products = Product.objects.all()

    # 해당 카테고리의 상품들
    p_comments = Product_Comment.objects.none()
    for product in products:
        p_comments = p_comments | Product_Comment.objects.select_related().filter(product_id=product.id)

    # 키워드 필터
    search_comments = Product_Comment.objects.none()
    keyword = request.GET.get('keyword')
    print(keyword)
    if keyword != "":
        for comment in p_comments:
            if keyword in comment.content or keyword in comment.product.name:
                search_comments = search_comments | comment
    else:
        keyword = ''
        search_comments = p_comments

    # 정렬 필터
    order = request.GET.get('order')
    if order == "score up":
        pass
    else:
        order = ""
    p_comments = search_comments
    print(len(p_comments))

    page = request.GET.get('page')
    if not page:
        page = '1'

    p = Paginator(p_comments, 10)

    pp_c = p.page(page)

    start_page = (int(page) - 1) // 10 * 10 + 1
    end_page = start_page + 9

    if end_page > p.num_pages:
        end_page = p.num_pages

    context = {
        'pp_c': pp_c,
        'pagination': range(start_page, end_page + 1),
        'p_comments': p_comments,
        'category': category,
        'keyword': keyword,
        'order': order,
        'page': page,
    }
    # return render(request, 'app/blog.html', { 'p_comments': p_comments, 'category': category })
    return render(request, 'app/blog.html', context)

def contact(request):
    return render(request, 'app/contact.html')


def icons(request):
    return render(request, 'app/icons.html')


def index(request):
    products = Product.objects.all()
    comments = Product_Comment.objects.all()
    beer_num, wine_num, cock_num, review_num = 0, 0, 0, 0

    for product in products:
        if product.category_id == 1:
            beer_num += 1
        elif product.category_id == 2:
            wine_num += 1
        else:
            cock_num += 1

    for _ in comments:
        review_num += 1
    context = {'beer_num':beer_num, 'wine_num':wine_num, 'cock_num':cock_num, 'review_num':review_num}

    return render(request, 'app/index.html', context)


# 추천 페이지에 맥주 데이터 가져오기 (16개)
def recommand(request):
    products = Product.objects.order_by('?')[:16]

    return render(request, 'app/recommand.html', {
        'products': products
    })

# @csrf_exempt
# def board_write(request):
#     if request.method == 'GET':
#         if request.session.get('email'):
#             return render(request, 'app/freewrite.html', {})
#         else:
#             return redirect('/login/')
#     else:
#         if request.session.get('email'):
#             email = request.session.get('email')
#             print(email)
#             user = User.objects.get(email=email)

#             title = request.POST.get('title')
#             print(title)
#             contents = request.POST.get('contents')
#             print(contents)
#             category_id = request.POST.get('category')
#             print(category_id)
#             try:
#                 b = Board(title=title, content=contents, category_id=category_id, user_id=user.id)
#                 # b.save()
#             except:
#                 return render(request, 'app/board.html', {})
#         else:
#             return render(request, 'app/login.html', {})

# 추천 페이지 결과를 이용 -> 머신러닝(클러스터링) -> 결과값과 동일한 군집의 제품 데이터 가져오기 (16개)
def recommand_result(request):
    # 머신러닝 나온 군집 안의 제품으로 줘야 함
    cluster = int(request.session.get('cluster'))

    products = Product.objects.filter(kmeans=cluster).order_by('?')[:16]

    for product in products:
        print(product.kmeans)

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
    keyword = request.GET.get('keyword')

    products = Product.objects.none()
    if category:
        category_id = Category.objects.get(name=category)
        products = Product.objects.filter(category_id=category_id)
    else:
        category = ""
        products = Product.objects.all()

    if keyword:
        products = products.filter(name__icontains=keyword)
    else:
        keyword = ""

    page = request.GET.get('page')

    if not page:
        page = '1'

    p = Paginator(products, 9)

    p_c = p.page(page)

    start_page = (int(page) - 1) // 10 * 10 + 1
    end_page = start_page + 9

    if end_page > p.num_pages:
        end_page = p.num_pages


    return render(
        request, 'app/product.html', {
            'p_c': p_c,
            'pagination': range(start_page, end_page + 1),
            'product_list': products,
            'category': category,
            'keyword': keyword
        })


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

            # db에 저장
            user.alias = nickname
            user.password = password
            user.save()

            # session에 재저장
            request.session['alias'] = nickname

            result = "Success"
            messages = "Profile change succeeded."
            return JsonResponse({'result': result, 'messages': messages})

        except:
            result = "Fail"
            messages = "Profile change failed."
            return render(request, 'app/login.html', {'messages' : messages})



def to_members_form(request):
    return render(request, 'app/to_members.html')


def userpage(request):
    email = request.GET.get('email')

    user = User.objects.get(email=email)

    user_comments = Product_Comment.objects.filter(user_id=user.id).select_related('product')

    page = request.GET.get('page')

    if not page:
        page = '1'

    p = Paginator(user_comments, 10)

    u_c = p.page(page)

    start_page = (int(page) - 1) // 10 * 10 + 1
    end_page = start_page + 9

    if end_page > p.num_pages:
        end_page = p.num_pages

    return render(request, 'app/userpage.html', {
        'u_c' : u_c,
        'pagination' : range(start_page, end_page + 1),
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
        print(id)

        try:
            member = User.objects.get(email=email,password=password)
        except:
            messages = "실패"
            return render(request, 'app/login.html', {'messages' : messages})
        else:
            request.session['email'] = email
            request.session['user_id'] = member.id
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

def find_password(request):
    if request.method == 'GET':
        return render(request, 'app/findpass.html', {})
    else:
        email = request.POST['email']

        try:
            user = User.objects.get(email=email)
        except:
            messages = "실패"
            return render(request, 'app/findpass.html', {'messages' : messages, 'email': email })
        else:
            messages = "성공"
            return render(request, 'app/findpass.html', {'messages' : messages , 'password' : user.password[:3] + '*' * (len(user.password) - 3) } )
