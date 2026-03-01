from django.urls import path  # URL 패턴 등록 함수
from . import views  # views.py 모듈
from django.contrib.auth import views as auth_views  # Django 기본 인증 관련 Views

app_name = 'uauth'  # URL 네임스페이스

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='uauth/login.html'), name='login'),  # 로그인 페이지
    path('logout/', views.logout, name='logout'),  # 로그아웃 처리
    path('signup/', views.signup, name='signup'),  # 회원가입 처리
    path('check_username/', views.check_username, name='check_username'),  # 아이디 중복 확인 처리
]