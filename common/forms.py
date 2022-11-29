from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserInfo


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {
            'username': '아이디',
            'password1': '비밀번호',
            'password2': '비밀번호 확인',
        }

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields =  ('gender', 'birthday')
        labels = {
            'gender': '성별',
            'birthday': '생년월일',
        }