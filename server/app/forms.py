from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from .models import User


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['photo', 'alias', 'password']

class LoginForm(forms.Form):
    user_id = forms.CharField(
        widget=forms.TextInput(
        attrs={'class': 'form-control',}), 
        error_messages={'required': '아이디을 입력해주세요.'},
        max_length=17,
        label='email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
        attrs={'class': 'form-control',}), 
        error_messages={'required': '비밀번호를 입력해주세요.'},
        label='password'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if user_id and password:
            try:
               user = User.objects.get(email=user_id)
            except User.DoesNotExist:
                self.add_error('user_id', '아이디가 존재하지 않습니다.')
                return
            