from django.urls import path  # URL 패턴 등록 함수
from . import views  # views.py 모듈

app_name = 'qna'  # URL 네임스페이스

urlpatterns = [
    path('', views.index, name='index'),  # qna 메인 목록 페이지
    path('question/<int:question_id>', views.question_detail, name='question_detail'),  # 질문 상세 페이지
    path('question/create', views.question_create, name='question_create'),             # 질문 작성 페이지
    path('question/modify/<int:question_id>', views.question_modify, name='question_modify'),  # 질문 수정 처리
    path('question/delete/<int:question_id>', views.question_delete, name='question_delete'),  # 질문 삭제 처리
    path('question/vote/<int:question_id>', views.question_vote, name='question_vote'),        # 질문 추천 처리
    
    path('answer/create/<int:question_id>', views.answer_create, name='answer_create'),  # 답변 작성 처리
    path('answer/modify/<int:answer_id>', views.answer_modify, name='answer_modify'),    # 답변 수정 처리
    path('answer/delete/<int:answer_id>', views.answer_delete, name='answer_delete'),    # 답변 삭제 처리
    path('answer/vote/<int:answer_id>', views.answer_vote, name='answer_vote'),          # 답변 추천 처리
]