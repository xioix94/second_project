from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import re
from app.models import User

def email_valid_duplicate(request):
    email = request.GET.get('email')
    ok1 = 'ok'
    ok2 = 'ok'
    final_ok = 'ok'
    a = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    result = a.match(email)
    if not result:
        ok1 = 'not ok'

    #데이터 베이스 조회
    users = User.objects.all()
    for user in users:
        if user.email == email:
            ok2 = 'not ok'
            break
   
    if ok1 == 'not ok' or ok2 == 'not ok':
        final_ok = 'not ok'
    
    return JsonResponse({
        'result': final_ok
    })


def email_valid(email):
    email_test = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    if not email_test.match(email):
        return False
    return True


def alias_valid(request):
    ok = 'ok'
    return JsonResponse({
        'result': ok
    })

def register(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    alias = request.POST.get('alias')
    sex = request.POST.get('sex')
    adult = request.POST.get('adult')

    print(email, password, password2, alias, sex, adult)

    
    if not email_valid(email):
        print("email not valid")
        return redirect("/register")


    return redirect('/login_form')

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
