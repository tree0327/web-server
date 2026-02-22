from django.db import models
from django.contrib.auth.models import User  # Django 기본 사용자 모델
from django.contrib.auth.forms import UserCreationForm  # Django 기본 회원가입 폼
from django import forms

class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # User와 1:1로 연결되는 추가정보 모델
    birthday = models.DateField(null=True, blank=True)   # 생년월일 (비워둘 수 있음)
    profile = models.ImageField(upload_to='profiles/', null=True, blank=True)  # 사용자 프로필 이미지 (비워둘 수 있음)

# Django Model Form 클래스
class UserForm(UserCreationForm):
    birthday = forms.DateField(label='Birthday', required=False)  # 생년월일 입력 필드 (선택)
    profile = forms.ImageField(label='profile', required=False)    # 프로필 이미지 입력 필드 (선택)

    class Meta:
        model = User  # User 모델 기반 회원가입 폼
        fields = ['username', 'password1', 'password2', 'email']  # 회원가입 폼에 포함될 필드