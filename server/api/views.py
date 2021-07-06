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
    password = request.POST.get('pw1')
    password2 = request.POST.get('pw2')
    alias = request.POST.get('alias')
    sex = request.POST.get('sex')

    return JsonResponse({'result' : True})

def register(request):
    try:
        print("register")
        # submit 접근처리
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('pw1')
        print(password)
        password2 = request.POST.get('pw2')
        print(password2)
        alias = request.POST.get('alias')
        print(alias)
        sex = request.POST.get('sex')
        print(sex)

        # 이메일 검증 구현
        if not email_valid(email) or not email_duplicate(email):
            return redirect("/register")
        
        # 비밀번호 비교
        if password != password2:
            return redirect("/register")
        
        # 비밀번호 암호화
        password = password.encode('utf-8')                 # 입력된 패스워드를 바이트 형태로 인코딩
        password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())  # 암호화된 비밀번호 생성
        password_crypt = password_crypt.decode('utf-8')             # DB에 저장할 수 있는 유니코드 문자열 형태로 디코딩
        
        # 닉네임 비교
        users = User.objects.all()
        for user in users:
            if user.alias == alias:
                return redirect("/register")

        User.objects.create(email=email, password=password_crypt, alias=alias, sex=sex)
        
        result = "ok"
        message = "Success to register"

        return JsonResponse({'result': result, 'message': message})
        
    except:
        result = "Fail"
        message = "Fail to register"
        return JsonResponse({'result': result, 'message': message})



@csrf_exempt
def submit_recommand_ml(request):
    selected_list_string = request.POST.get('selected_list')
    selected_list = list(map(int, selected_list_string.split('-')))

    cluster = -1
    count = 0
    bd, sp, sw, tan, acid, alc = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    comments = Product_Comment.objects.select_related('product')
    for comment in comments:
        alc_temp = comment.product.alcohol
        if comment.product_id in selected_list:
            count += 1
            bd += comment.bold
            sp += comment.sparkling
            sw += comment.sweet
            tan += comment.tannic
            acid += comment.acidic
            alc += alc_temp
    bd /= count
    sp /= count
    sw /= count
    tan /= count
    acid /= count
    alc /= count
    # 군집값 리스트, 선택값들의 평균에 대한 군집 반환
    cluster = clustering.return_cluster([bd, sp, sw, tan, acid, alc])
    
    request.session['cluster'] = str(cluster)

    return JsonResponse({'result': 'ok'})
