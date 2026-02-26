"""
URL configuration for _04_qna project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin  # Django 관리자 기능
from django.urls import path, include  # URL 등록 함수
from django.views.generic import RedirectView  # 특정 경로로 리다이렉트하는 뷰

from django.conf import settings  # settings.py 값 사용
from django.conf.urls.static import static  # 개발환경에서 미디어 파일 경로 연결하기 위한 함수

urlpatterns = [
    path('admin/', admin.site.urls),  # 관리자 페이지 url
    path('', RedirectView.as_view(url='/qna/', permanent=False), name='index'),  # 루트 접속 시 /qna/로 이동
    path('qna/', include('qna.urls')),  # qna 앱의 urls.py 연결
    path('uauth/', include('uauth.urls')),  # uauth 앱의 urls.py 연결
]

# 업로드한 파일 경로 설정
# django는 원래 정적파일을 서비스하지 않음. 개발환경에서만 처리하도록 설정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
