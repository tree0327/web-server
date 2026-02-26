from django.shortcuts import render, redirect  # 템플릿 응답, 페이지 이동 처리
from django.contrib.auth import logout as auth_logout  # Django 기본 로그아웃 함수
from django.contrib.auth import login as auth_login    # Django 기본 로그인 함수
from django.contrib.auth import authenticate   # 사용자 인증 함수
from .models import UserForm, UserDetail     # 회원가입 폼, 사용자 상세정보 모델
from django.db import transaction            # DB 트랜잭션 처리 도구
from django.contrib.auth.models import User  # Django 기본 사용자 모델
from django.http import JsonResponse         # JSON 응답 처리

# 현재 로그인한 사용자를 로그아웃시키는 함수
def logout(request):
    auth_logout(request)  # 세션 정보를 삭제하고, 로그아웃 처리
    return redirect('index')  # 메인페이지로 이동

# 트랜잭션 하위에서 예외가 발생하면 모든 DML 작업이 롤백됨
# @transaction.atomic

# 회원가입 처리 후 추가정보 저장과 자동 로그인까지 수행하는 함수
def signup(request):
    if request.method == 'POST':    # 회원가입 폼 제출 요청인 경우
        form = UserForm(request.POST, request.FILES)  # 일반 데이터와 파일 데이터를 폼에 바인딩
        if form.is_valid():
            # 트랜잭션 블럭 : 내부 DB 조작은 트랜잭션 적용
            with transaction.atomic():
                # User 모델 저장 -> auth_user 테이블에 저장
                user = form.save(commit=True)  # User 객체를 생성하고 DB에 저장
                
                # UserDetail 모델 저장 -> uauth_userdetail 테이블에 저장
                user_detail = UserDetail(
                    user = user,  # 방금 생성한 User와 연결
                    birthday = form.cleaned_data.get('birthday'),  # 정제된 생년월일 데이터 저장
                    profile = form.cleaned_data.get('profile')     # 업로드된 프로필 이미지 저장
                )
                
                user_detail.save()  # UserDetail 정보 DB 저장
            
            print(f'회원가입 완료: {user_detail}')

            # 회원가입 후 로그인 처리
            username = form.cleaned_data.get('username')  # 입력한 아이디
            raw_password = form.cleaned_data.get('password1')  # 입력한 비밀번호
            
            user = authenticate(username=username, password=raw_password)  # 사용자 인증 수행
            
            auth_login(request, user)  # 인증된 사용자 로그인 처리
            return redirect('index')
    else:
        form = UserForm()  # GET 요청이면 빈 회원가입 폼 생성
    
    return render(request, 'uauth/signup.html', {'form': form})  # 회원가입 페이지 렌더링

# 전달받은 username의 중복 여부를 JSON으로 반환하는 함수
def check_username(request):
    username = request.GET.get('username')  # 요청 파라미터에서 username 값 추출
    is_exists = User.objects.filter(username=username).exists()  # 동일한 username 존재 여부 확인

    if is_exists:
        return JsonResponse({'available': False, 'message': '이미 사용중인 아이디입니다.'})  # 사용 불가 응답
    
    return JsonResponse({'available': True, 'message': '사용 가능한 아이디입니다.'})  # 사용 가능 응답