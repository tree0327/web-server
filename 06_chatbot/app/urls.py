from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),  # 메인 페이지 요청
    path('init_conversation/', views.init_conversation, name='init_conversation'),  # 새 대화 세션 생성
    path('chatbot/', views.chatbot, name='chatbot'),  # 챗봇 응답
    path('remove_conversation/', views.remove_conversation, name='remove_conversation'),  # 대화 세션 삭제
    path('get_session_list/', views.get_session_list, name='get_session_list'),     # 저장된 세션 목록 조회
    path('restore_conversation/', views.restore_conversation, name='restore_conversation'),  # 이전 대화 세션 복원
]