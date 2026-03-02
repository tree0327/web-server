# models.py : DB 구조 설계 + ORM 매핑 (객체 <-> 테이블 연결)
# -> 이 구조의 테이블을 Django ORM이 생성하고 관리하도록 맡기겠다.
# python manage.py makemigrations : models.py에서 정의한 테이블 구조대로 DB에 생성하기 위한 변경 기록 파일
# python manage.py migrate : 생성된 migration 파일을 실제 DB에 적용

from django.db import models  # Django ORM 모델 클래스 생성 모듈

class Post(models.Model):
    title = models.CharField(max_length=100)  # 최대 100자 문자열 필드
    content = models.TextField()  # 텍스트 필드
    created_at = models.DateTimeField(auto_now_add=True)  # 최초 생성 시간을 자동 저장하는 필드
    updated_at = models.DateTimeField(auto_now=True)  # 수정시 현재 시간을 자동 저장하는 필드
    
    # 객체를 문자열로 표현할 때 사용
    def __str__(self):
        return self.title  # 객체 출력시 제목 문자열 반환