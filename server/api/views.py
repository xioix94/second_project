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


def alias_valid(request):
    ok = 'ok'
    return JsonResponse({
        'result': ok
    })


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