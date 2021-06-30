from django.shortcuts import render
from django.http import JsonResponse
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