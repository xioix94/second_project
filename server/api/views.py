from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import re
from app.models import User
from django.views.decorators.csrf import csrf_exempt
from app.models import Product_Comment, Product
from . import clustering
import bcrypt

def email_valid(email):
    # 정규식 검사기
    email_test = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    if not email_test.match(email):
        return False
    return True

def email_duplicate(email):
    #데이터 베이스 조회
    users = User.objects.all()
    for user in users:
        if user.email == email:
            return False
    return True

def adult_valid(data):
    return True

@csrf_exempt
def email_check(request):
    # email 검증 및 중복체크 ajax 처리
    email = request.POST.get('email')

    if email_valid(email) and email_duplicate(email):
        return JsonResponse({'result': 'ok'})

    return JsonResponse({'result': 'not ok'})

@csrf_exempt
def password_valid(request):
    # 비밀번호 중복 체크
    pw1 = request.POST.get('pw1')
    pw2 = request.POST.get('pw2')

    if pw1 != pw2:
        return JsonResponse({'result' : 'not ok'})
    return JsonResponse({'result' : 'ok'})

@csrf_exempt
def alias_valid(request):
    alias = request.POST.get('alias')
    #데이터 베이스 조회
    users = User.objects.all()
    for user in users:
        if user.alias == alias:
            return JsonResponse({'result' : 'not ok'})
    return JsonResponse({'result' : 'ok'})

@csrf_exempt
def adult_value(request):
    if request.POST.get('adult'):
        return JsonResponse({'result' : 'not ok'})
    return JsonResponse({'result' : 'ok'})

@csrf_exempt
def submit_valid(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    alias = request.POST.get('alias')
    sex = request.POST.get('sex')

    return True

def register(request):
    # submit 접근처리
    email = request.POST.get('email')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    alias = request.POST.get('alias')
    sex = request.POST.get('sex')
    adult = request.POST.get('adult')

    # password=bcrypt.hashpw(password,bcrypt.gensalt())
    
    '''
    모델에서 저장된거 받아온 pw

    pw.checkpw()
    
    '''
    # 성별 치환
    if sex == 'men':
        sex = 0
    else:
        sex = 1

    # 이메일 검증 구현
    if not email_valid(email) or not email_duplicate(email):
        return redirect("/register")
    # 비밀번호 비교
    if password != password2:
        return redirect("/register")
    # 닉네임 비교
    users = User.objects.all()
    for user in users:
        if user.alias == alias:
            return redirect("/register")
    # 성인 확인
    if not adult:
        return redirect("/register")

    User.objects.create(email=email, password=password, alias=alias, sex=sex)

    return redirect("/login")


def login(request):
    if request.method == 'GET':
        return render(request, 'app/login_check.html', {})
    else:
        user_id = request.POST['email']
        user_pw = request.POST['password']

        try:
            member = User.objects.get(email=user_id,password=user_pw)
        except:
            return HttpResponse('로그인 실패')
        else:
            # request.session['email'] = user_id
            return HttpResponse('로그인 성공')

@csrf_exempt
def submit_recommand_ml(request):
    selected_list_string = request.POST.get('selected_list')
    selected_list = list(map(int, selected_list_string.split('-')))


    cluster = -1
    count = 0
    bd, sp, sw, tan, acid, alc = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    comments = Product_Comment.objects.select_related('product')
    for comment in comments:
        count += 1
        alc = comment.product.alcohol
        if comment.product_id in selected_list:
            bd += comment.bold
            sp += comment.sparkling
            sw += comment.sweet
            tan += comment.tannic
            acid += comment.acidic
    bd /= count
    sp /= count
    sw /= count
    tan /= count
    acid /= count
    
    # 군집값 리스트, 선택값들의 평균에 대한 군집 반환
    cluster = clustering.return_cluster([bd, sp, sw, tan, acid, alc])
    
    request.session['cluster'] = str(cluster)

    return JsonResponse({'result': 'ok'})
