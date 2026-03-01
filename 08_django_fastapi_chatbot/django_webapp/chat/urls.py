from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_view, name='chat'),  # 채팅 메인 페이지
    path('send_message/', views.send_message, name='send_message'),  # 메시지 전송 요청
    path('get_history/', views.get_history, name='get_history'),     # 대화 이력 조회 요청
]