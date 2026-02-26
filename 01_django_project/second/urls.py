from django.urls import path      # url 경로 정의 & 연결
from . import views

app_name = 'second'  # URL namespace 이름 지정

urlpatterns = [
    path('', views.index, name='index'),  # /second/ 요청을 index 뷰(함수)와 연결
]