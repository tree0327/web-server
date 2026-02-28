from django.shortcuts import render, redirect
from datetime import datetime

def index(request):
    return render(request, 'app/index.html')

# 세션에 여러 종류의 데이터를 저장해서 테스트
def set_session(request):
    username = request.POST.get('username')  # 사용자 입력값
    request.session['username'] = username  # username 세션 저장

    # 여러 종류의 정보를 세션 객체에 저장
    request.session['point'] = 1234567890
    request.session['prob'] = 0.12345
    request.session['expired'] = True
    request.session['nums'] = [1, 2, 3, 4, 5]
    request.session['data'] = {
        'message': 'Hello, Django Session!!!',
        'today': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    return redirect('app:index')  # 저장 후 메인 페이지로 이동

# 기존 세션값을 수정하거나 삭제하는 함수
def modify_session(request):
    # 새 속성 추가/변경
    # - 세션 객체의 최상위키 변경은 자동으로 감지
    request.session['favorite_color'] = 'springgreen'  # 새로운 세션 데이터 추가

    # - 중첩된 속성 변경시에는 명시적으로 변경됨을 알려야 함.
    request.session['nums'].append(999)
    request.session['data']['new_item'] = '새로운 아이템'

    request.session.modified = True  # 중첩 데이터 변경 사항 저장 표시

    del request.session['point']  # 세션 데이터 삭제

    return redirect('app:index') 

# 현재 세션 전체를 삭제하는 함수
def delete_session(request):
    request.session.flush()  # 세션 데이터와 세션 쿠키를 모두 삭제
    return redirect('app:index') 

def set_cookie(request):
    # 쿠키는 response객체에서 굽는다.
    name = request.POST.get('cookie_name')
    value = request.POST.get('cookie_value')

    response = redirect('app:index')
    response.set_cookie(
        name, value,       # 쿠키 이름, 값
        path = '/app/',    # /app 하위 경로 요청에서만 쿠키 전송
        max_age = 120,     # 120초 동안 유지
        httponly = True,   # JS에서 접근 불가
        samesite = 'Lax',  # 외부 사이트 요청시 쿠키 전송 제한
        secure = False     # HTTPS 전용 여부 X (개발용)
    )

    return response

def delete_cookie(request):
    response = redirect('app:index')  # 응답 객체 생성
    name = request.POST.get('cookie_name')  # 쿠키 이름 입력값
    response.delete_cookie(name, path='/app/')  # 지정한 경로 기준으로 쿠키 삭제

    return response
