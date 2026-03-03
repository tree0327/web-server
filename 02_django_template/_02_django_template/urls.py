"""
URL configuration for _02_django_template project.

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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # 특정 URL을 다른 주소로 이동시키는 제네릭 뷰

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/app/', permanent=False)),  # 루트(/) 요청을 /app/으로 임시 리다이렉트
    path('app/', include('app.urls')),  # /app/ 경로로 들어온 요청은 app 앱의 urls.py에서 처리
]