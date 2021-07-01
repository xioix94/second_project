from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import re
from app.models import User
from django.views.decorators.csrf import csrf_exempt

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

def register(request):
    # submit 접근처리
    email = request.POST.get('email')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    alias = request.POST.get('alias')
    sex = request.POST.get('sex')
    adult = request.POST.get('adult')

    # 이메일 검증 구현
    if not email_valid(email) or not email_duplicate(email):
        return redirect("/register")

    # 비밀번호, 비밀번호 확인 검증 미구현
    if not password_valid(password):
        return redirect('/register')
    
    # 성인 체크 미구현
    if not adult_valid(adult):
        return redirect('/register')



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
