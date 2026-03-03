from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),  # 메인 페이지 요청
    path('set_session/', views.set_session, name='set_session'),           # 세션 저장 처리
    path('modify_session/', views.modify_session, name='modify_session'),  # 세션 수정 처리
    path('delete_session/', views.delete_session, name='delete_session'),  # 세션 삭제 처리
    path('set_cookie/', views.set_cookie, name='set_cookie'),              # 쿠키 저장 처리
    path('delete_cookie/', views.delete_cookie, name='delete_cookie'),     # 쿠키 삭제 처리
]