# python manage.py shell
from post.models import Post  # Post 모델

Post  # Post 모델 클래스 확인
Post.objects  # Post 모델의 매니저 객체
Post.objects.all()  # 전체 Post 조회
queryset = Post.objects.all()  # 조회 결과를 queryset에 저장
str(queryset.query)  # 실행될 SQL 쿼리 문자열 확인

# Post 데이터 생성
post = Post.objects.create(title='Hello World', content='🍭🍭🍭🍭🍭')  # 객체 생성 + 변수 저장
post  # 객체 확인
# 객체 내 필드 값 확인
post.id
post.title
post.content
post.created_at
post.updated_at

post2 = Post(title='배고프다', content='춥고 배고프고 졸립다!')  # Post 객체 생성
post2.save()  # 해당 객체를 DB에 저장
# 객체 내 필드 값 확인
post2.id
post2.title
post2.content
post2.created_at
post2.updated_at

# Post 데이터 조회
queryset = Post.objects.all()  # 전체 Post 조회
queryset  # 조회 결과

# 쿼리 확인 : 1. queryset.query
queryset.query        # Query 객체
str(queryset.query)   # SQL 문자열로 변환

import sqlparse  # SQL 포맷팅 라이브러리
print(sqlparse.format(str(queryset.query), reindent=True))  # SQL을 정렬(들여쓰기)

# 쿼리 확인 : 2. connection.queries
from django.db import connection  # 실행된 SQL 목록 확인

connection.queries      # 실행된 모든 쿼리
connection.queries[-1]  # 마지막 쿼리

# WHERE 조건 검색
# 1. filter  : 조건에 맞는 여러 개의 데이터를 QuerySet 형태로 조회
# 2. get     : 조건에 맞는 단일 데이터를 조회 (0개 또는 여러 개면 오류 발생)
# 3. exclude : 지정한 조건에 해당하는 데이터를 제외하고 조회

# 특정 조건에 맞는 데이터 필터링
Post.objects.filter(title='배고프다')  # 여러 행
Post.objects.get(title='배고프다')     # 단일 행

# 문자열 필드
Post.objects.filter(title='Hello world')        # title이 'Hello world'인 데이터
Post.objects.filter(title__startswith='Hello')  # title이 'Hello' 로 시작하는 데이터
Post.objects.filter(title__endswith='!')        # title이 '!' 로 끝나는 데이터
Post.objects.filter(content__contains='🍭')     # content가 '🍭'을 포함하는 데이터
Post.objects.filter(title__icontains='happy')   # title이 'happy'을 포함하는 데이터 (대소문자 구분없이)
Post.objects.filter(content__isnull=True)       # content가 null인 데이터

# 날짜 필드
Post.objects.filter(created_at__lte='2027-01-01')  # 2027-01-01 이전 날짜 데이터
Post.objects.filter(created_at__gt='2026-01-01')   # 2026-01-01 이후 날짜 데이터
Post.objects.filter(created_at__gt='2026-03-14 00:00:00')  # 특정 일시 이후 날짜 데이터
Post.objects.filter(created_at__year=2026)         # 생성연도가 2026년인 데이터

# 여러 조건 AND
Post.objects.filter(title='Hello world', created_at__year=2026)  # 조건을 AND로 적용
Post.objects.filter(title='Hello world').filter(created_at__year=2026)  # filter 체이닝으로 AND 적용

# 여러 조건 OR (Q 객체를 | 연산자로 연결)
from django.db.models import Q  # 복합 조건식 객체 Q
Post.objects.filter(Q(title__contains='🍭') | Q(content__contains='🍭'))  # OR 조건

# NOT 비교
# - exclude      : 지정한 조건에 해당하는 데이터를 제외하고 조회
# - filter(~Q()) : Q 객체에 NOT 연산자를 적용해 조건을 반대로 하여 조회

# 같은 행의 다른 컬럼 비교시 F객체 사용
from django.db.models import F
Post.objects.exclude(created_at=F('updated_at'))     # created_at과 updated_at 같은 데이터 제외
Post.objects.filter(~Q(created_at=F('updated_at')))  # created_at과 updated_at이 다른 데이터 조회

# 정렬
Post.objects.all().order_by('created_at')   # 생성일 오름차순
Post.objects.all().order_by('-created_at')  # 생성일 내림차순
Post.objects.all().order_by('title', 'id')  # title 정렬, 같은값이면 id 정렬

# 한 행 조회 : get (주로 pk컬럼 조회시 사용)
Post.objects.get(id=1)     # id가 1인 객체
Post.objects.get(id=100)   # id가 100인 객체 (없어서 오류)
Post.objects.filter(id=1)  # id가 1인 객체 (QuerySet 형태)

# 기존 Post 객체와 새롭게 질문한 뒤 반환받은 객체와 내용 비교
post = Post.objects.get(id=1)   # id가 1인 객체
post == Post.objects.get(id=1)  # 기존 객체와 새로운 객체 비교 (True)
Post.objects.get(id=1) is post  # 같은 메모리 객체인지 비교 (False)
id(Post.objects.get(id=1)), id(post)  # 메모리 주소값 확인 (다름)

# value : 특정 필드만 딕셔너리 형태의 쿼리셋 생성 
Post.objects.values('title', 'content')  # title, content만 dict 형태로 조회
Post.objects.values()  # 모든 필드를 key-value 형태로 조회
Post.objects.values('title', 'content').distinct()  # title, content만 dict 형태로 중복 제거 후 조회

# groupby : values + annotate
from django.db.models.functions import ExtractYear
from django.db.models import Count
# created_at에서 연도만 뽑아서, 그 연도별로 데이터 갯수를 센다. (연도별 데이터 개수 집계)
Post.objects.annotate(year=ExtractYear('created_at')).values('year').annotate(count_by_year=Count('year'))

# Post 수정
post = Post.objects.get(id=1)  # id가 1인 객체 조회
post.title   # 수정 전
post.title += '123'  # 제목 뒤에 123 추가
post.title   # 수정 후
post.save()  # DB에 반영

# Post 삭제
post = Post.objects.create(title='Hello~', content='World~')  # 객체 생성
post.delete()  # 객체 삭제