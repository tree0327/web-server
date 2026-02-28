from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.upload_file, name='upload'),  # 루트 경로 요청을 파일 업로드 views 함수로 연결
]