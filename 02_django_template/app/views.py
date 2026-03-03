from django.shortcuts import render
from datetime import datetime

context = {
    'name': 'Django',
    'age': 13,
    'num': 1,
    'hobby': ['coding', 'reading', 'traveling'],
    'today': datetime.now(),
    'is_authenticated': False,
    'fruits': ['apple', 'banana', 'cherry'],
    'users': [
        {'id': 1234, 'name': 'Alice', 'age': 24, 'married': True},
        {'id': 2345, 'name': 'Bob', 'age': 34, 'married': False},
        {'id': 3456, 'name': 'Charlie', 'age': 25, 'married': True},
    ],
    # 'users': [],
}

# /app/ 요청시 index 템플릿을 반환하는 뷰 함수
def index(request):
    return render(request, 'app/index.html')  # index 템플릿 렌더링

# 템플릿 변수와 필터 예제 페이지 반환하는 뷰 함수
def _01_variables_filters(request):
    context['today'] = datetime.now()  # 현재시간으로 갱신
    return render(request, 'app/01_variables_filters.html', context) # 템플릿과 context 전달

# 템플릿 태그 사용 페이지를 반환하는 뷰 함수
def _02_tags(request):
    return render(request, 'app/02_tags.html', context)

# 템플릿 상속 페이지를 반환하는 뷰 함수
def _03_layout(request):
    return render(request, 'app/03_layout.html')

# sttic 파일(CSS, JS, 이미지)를 사용
def _04_static_files(request):
    return render(request, 'app/04_static_files.html')

# URL 태그 및 reverse 사용
def _05_urls(request):
    return render(request, 'app/05_urls.html')

# 게시글 id를 받아 상세 페이지 요청을 처리하는 함수
def articles_detail(request, id):
    # print(f'{id = }')
    return render(request, 'app/05_urls.html')

# 게시글 카테고리와 id를 받아 요청을 처리하는 함수
def articles_category(request, category, id):
    # print(f'{category = }, {id = }')
    return render(request, 'app/05_urls.html')

# 검색 요청(GET 방식)을 처리하는 뷰 함수
def search(request):
    # print(request.GET.urlencode())  # 쿼리스트링 전체 출력
    # print(request.GET)              # QueryDict 객체 출력
    q = request.GET.getlist('q', [])    # q라는 이름의 파라미터 여러개 가져옴
    lang = request.GET.get('lang', '')  # lang 파라미터 가져옴
    # print(f'{q = }, {lang = }')
    return render(request, 'app/05_urls.html', {'q': q, 'lang': lang})  # 템플릿에 값 전달

def _06_bootstrap(request):
    return render(request, 'app/06_bootstrap.html')

def myBootstrap(request):
    return render(request, 'app/myBootstrap.html')