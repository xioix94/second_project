from django.shortcuts import render
from django.http import JsonResponse
import re
from app.models import User

# 이메일 검증
def email_valid(request):
    email = request.GET.get('email')

    ok = 'ok'
    a = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    result = a.match(email)
    if not result:
        ok = 'not ok'

    return JsonResponse({
        'result': ok
    })

def email_duplicate(request):
    email = request.GET.get('email')
    ok = 'ok'
    
    #데이터 베이스 조회
    users = User.objects.all()
    for user in users:
        if user.email == email:
            ok = 'not ok'
            break

    return JsonResponse({
        'result': ok
    })