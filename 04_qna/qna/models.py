from django import forms  # Django From 기능
from django.db import models  # Django Model 기능
from django.contrib.auth.models import User  # Django 기본 사용자 모델

class Question(models.Model):
    # 작성자 : 회원 삭제 시 작성자는 Null 처리
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='questions')
    subject = models.CharField(max_length=200)  # 질문 제목 (최대길이 200자)
    content = models.TextField()  # 질문 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 최초 작성일시 자동 저장
    modified_at = models.DateTimeField(auto_now=True)     # 수정일시 자동 갱신
    voters = models.ManyToManyField(User, related_name='question_votes')  # 질문 추천 사용자 목록

class Answer(models.Model):
    # 작성자 : 회원 삭제 시 작성자는 Null 처리
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # 어떤 질문의 답변인지 연결 (답변 생성시 삭제)
    content = models.TextField()  # 답변 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 최초 작성일시 자동 저장
    modified_at = models.DateTimeField(auto_now=True)     # 수정일시 자동 갱신
    voters = models.ManyToManyField(User, related_name='answer_votes')  # 답변 추천 사용자 목록

# Django Model Form 클래스
class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question  # Question 모델을 기반으로 폼 생성
        fields = ['subject', 'content']  # 폼에 포함할 필드
        labels = {
            'subject': '제목',
            'content': '내용',
        }  # 필드 제목