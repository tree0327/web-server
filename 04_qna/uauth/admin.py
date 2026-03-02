from django.contrib import admin  # Django 관리자 기능
from .models import UserDetail    # 관리자에 등록할 UserDetail 모델

admin.site.register(UserDetail)  # UserDetail 모델을 관리자 페이지에 등록