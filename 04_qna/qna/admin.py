from django.contrib import admin  # Django 관리자 기능
from .models import Question, Answer  # 관리자 기능에 등록한 모델

admin.site.register(Question)  # 관리자페이지에 Question 모델 등록
admin.site.register(Answer)    # 관리자페이지에 Answer 모델 등록