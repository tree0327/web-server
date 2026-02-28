# Django 세션(Session) & 쿠키(Cookie) 개념 노트

## 1. HTTP 무상태성(Statelessness)

### 개념

HTTP는 요청과 응답이 한 번 완료되면 서버가 클라이언트를 **완전히 잊어버린다**. 이를 무상태성(Statelessness)이라 한다.

> **비유**: 은행 창구 직원에게 볼일을 볼 때마다 "저는 홍길동입니다"라고 다시 소개해야 하는 상황과 같다. 직원은 이전 대화를 기억하지 못한다.

### 이 문제를 해결하는 두 가지 방법

| 방법 | 원리 | 비유 |
|------|------|------|
| **세션(Session)** | 서버 DB에 데이터를 저장하고, 브라우저에는 **열쇠(`sessionid`)만** 전달 | 짐 보관소에 짐을 맡기고 번호표만 가지고 다니는 것 |
| **쿠키(Cookie)** | 데이터 자체를 브라우저에 저장하고, 매 요청마다 서버로 전송 | 명함을 직접 들고 다니며 매번 제시하는 것 |

> **한 줄 요약**: 세션은 "열쇠만 클라이언트에", 쿠키는 "데이터 자체를 클라이언트에".

---

## 2. SessionMiddleware의 역할

### 개념

Django의 미들웨어(Middleware)는 요청이 뷰(View)에 도달하기 전, 그리고 응답이 브라우저로 나가기 전에 거치는 **관문 체인**이다.

`SessionMiddleware`는 이 체인 안에서 두 가지 일을 담당한다.

| 시점 | 동작 |
|------|------|
| **요청(Request) 시** | `sessionid` 쿠키를 읽어 DB에서 세션 데이터를 꺼낸 뒤 `request.session`에 붙여준다 |
| **응답(Response) 시** | 변경된 세션 데이터를 다시 DB에 저장한다 |

> **한 줄 요약**: `request.session`을 사용할 수 있는 이유가 바로 `SessionMiddleware` 덕분이다.

---

## 3. `django_session` 테이블 구조

### 개념

Django가 DB 기반 세션을 사용할 때 생성되는 테이블이다.
**"브라우저가 가진 열쇠(session_key)에 맞는 보관함(session_data)을 찾고, 유효기간(expire_date)을 확인하는 장소"**라고 정의할 수 있다.

### 테이블 구조 (3개 컬럼)

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| `session_key` | varchar(40) | Primary Key. 브라우저 쿠키의 `sessionid` 값과 일치하는 고유 ID |
| `session_data` | text | 사용자 세션 정보가 **인코딩(직렬화 + 서명)**되어 저장된 문자열 |
| `expire_date` | datetime | 세션 만료 일시. 이 시간이 지나면 세션은 무효 처리 |

### 동작 순서

```
① 브라우저가 sessionid=abc123 쿠키를 서버로 전송
② Django가 django_session 테이블에서 session_key='abc123' 행을 조회
③ session_data를 복호화하여 Python 딕셔너리(request.session)로 변환
   (expire_date가 현재 시간보다 과거면 무효 처리)
④ 뷰에서 session 데이터를 변경하면, 응답 시점에 다시 인코딩하여 저장
```

### 실제 저장 형태

```
session_key  : h5j28...9d2a  (40자 무작위 문자열)
session_data : eyJuYW1lIjoi... (Base64 인코딩 + 위변조 방지 서명이 붙은 긴 문자열)
expire_date  : 2026-03-05 23:11:00
```

> **참고**: 만료된 세션은 자동 삭제되지 않는다. `python manage.py clearsessions` 명령으로 정리한다.

---

## 4. 세션에 저장 가능한 자료형

### 개념

`request.session`은 Python 딕셔너리처럼 동작하며, **JSON으로 직렬화 가능한 모든 타입**을 저장할 수 있다.

| 저장 가능 타입 | 예시 | 비고 |
|--------------|------|------|
| `str` | `'홍길동'` | ✅ |
| `int` | `1234567890` | ✅ |
| `float` | `12345.678` | ✅ |
| `bool` | `True` | ✅ |
| `list` | `[1, 2, 3]` | ✅ |
| `dict` | `{'key': 'val'}` | ✅ |
| `datetime` | `datetime.now()` | ❌ → 문자열로 변환 후 저장 |

> **한 줄 요약**: JSON으로 표현 가능한 것은 모두 세션에 저장할 수 있다.

내부 저장 과정: `Python 객체` → JSON 직렬화 → 서명(위변조 방지) → DB 저장

---

## 5. 세션 읽기: context 전달 vs 템플릿 직접 접근

### 두 가지 방식 비교

Django 템플릿에서 세션 데이터에 접근하는 방법은 두 가지다.

| 방식 | 뷰 코드 | 템플릿 코드 | 평가 |
|------|---------|------------|------|
| **context 전달** (권장) | `context['username'] = session.get('username')` | `{{ username }}` | ✅ 뷰-템플릿 분리 원칙 준수. 템플릿이 세션 구조에 독립적 |
| **직접 접근** | (별도 처리 불필요) | `{{ request.session.username }}` | ⚠️ 편리하지만 템플릿이 세션 키 이름에 직접 의존 |

> **한 줄 요약**: 뷰에서 context로 전달하는 것이 Django 모범 사례(Best Practice)다.

---

## 6. 세션 만료 제어: `set_expiry()`

### 개념

`set_expiry(n)`은 세션의 만료 시간을 코드 수준에서 동적으로 제어하는 메서드다.
`settings.py`의 전역 설정(`SESSION_COOKIE_AGE`)을 **덮어씌운다**.

### 호출 위치가 중요하다

| 패턴 | 결과 |
|------|------|
| ❌ `index` 뷰에서 매 요청마다 호출 | 매 요청마다 타이머가 리셋 → 사실상 만료 안 됨 |
| ✅ 세션 생성 뷰에서 한 번만 호출 | 세션 생성 시점부터 n초 후 만료 |

### 주요 인자값

| 인자 | 동작 |
|------|------|
| `set_expiry(n)` | n초 후 만료 |
| `set_expiry(0)` | 브라우저를 닫으면 즉시 만료 (세션 쿠키) |
| `set_expiry(None)` | `settings.py`의 `SESSION_COOKIE_AGE` 값을 따름 |

> **한 줄 요약**: `set_expiry()`는 세션 데이터를 저장하는 뷰에서만 호출한다.

### `settings.py` 전역 세션 설정

| 설정값 | 기본값 | 설명 |
|--------|--------|------|
| `SESSION_ENGINE` | `'...backends.db'` | 세션 저장 방식 (DB 저장) |
| `SESSION_COOKIE_AGE` | `1209600` | 세션 유지 시간 (기본 2주, 초 단위) |
| `SESSION_EXPIRE_AT_BROWSER_CLOSE` | `False` | 브라우저 종료 시 세션 만료 여부 |
| `SESSION_SAVE_EVERY_REQUEST` | `False` | 변경 시에만 저장 (성능 최적화) |
| `SESSION_COOKIE_HTTPONLY` | `True` | JS 접근 차단 (XSS 방어) |
| `SESSION_COOKIE_SAMESITE` | `'Lax'` | 외부 사이트 POST 차단 (CSRF 방어) |

---

## 7. `session.modified` 플래그 — mutable 객체의 함정

### 개념

Django는 세션 딕셔너리의 **최상위 키가 교체될 때만** 자동으로 `modified = True`를 설정한다.
리스트나 딕셔너리의 **내부 값을 변경**하면 Django가 이를 감지하지 못하고, 변경 내용이 DB에 저장되지 않는다.

### 자동 감지 여부 비교

| 코드 | 감지 여부 | 이유 |
|------|----------|------|
| `session['username'] = '김철수'` | ✅ 자동 감지 | 최상위 키 교체 |
| `session['nums'] = [1, 2, 3, 99]` | ✅ 자동 감지 | 최상위 키 교체 |
| `session['nums'].append(99)` | ❌ 감지 불가 | 리스트 **내부** 값 변경 |
| `session['data']['msg'] = '변경'` | ❌ 감지 불가 | 딕셔너리 **내부** 값 변경 |

### 해결 방법

```python
# 리스트/딕셔너리 내부를 변경한 뒤 반드시 수동 설정
request.session['nums'].append(99)
request.session.modified = True  # ← 이 줄이 없으면 변경이 저장 안 됨
```

> **한 줄 요약**: 리스트·딕셔너리 내부 값을 바꿀 때는 `session.modified = True`를 수동으로 설정한다.

---

## 8. 세션 삭제: `del` vs `flush()`

### 두 가지 삭제 방법 비교

| 방법 | 동작 | `sessionid` 변경 | 사용 시점 |
|------|------|:-----------------:|---------|
| `del session['key']` | 지정한 키만 삭제. 나머지 데이터와 `sessionid` 유지 | ❌ | 특정 정보만 제거할 때 |
| `session.flush()` | 모든 데이터 삭제 + DB 레코드 삭제 + **새 `sessionid` 발급** | ✅ | 로그아웃 (보안상 세션 고정 공격 방어) |

### 로그아웃에는 반드시 `flush()`를 사용해야 하는 이유

`del`로만 사용자 데이터를 지우면 `sessionid` 쿠키값은 그대로 남는다.
공격자가 이미 `sessionid`를 탈취했다면, 로그아웃 후에도 세션을 재사용할 수 있다.
`flush()`는 서버에서 세션 레코드를 삭제하고 새 ID를 발급해 **탈취된 `sessionid`를 무력화**한다.

> **한 줄 요약**: 로그아웃 = `flush()`, 부분 삭제 = `del session['key']`.

---

## 9. 쿠키 설정: Request가 아닌 Response에서

### 핵심 차이

세션과 쿠키는 **쓰는 위치**가 다르다.

| 구분 | 쓰기 방법 | 이유 |
|------|----------|------|
| **세션** | `request.session['key'] = value` | `SessionMiddleware`가 응답 시 알아서 저장 |
| **쿠키** | `response.set_cookie('key', value)` | HTTP `Set-Cookie` 헤더가 **응답**에 담겨 브라우저로 전달되기 때문 |

### 올바른 쿠키 설정 순서

```python
# ✅ 올바른 패턴 (3단계)
response = redirect('app:index')        # ① Response 객체 먼저 생성
response.set_cookie('my_cookie', value) # ② Response에 쿠키 설정
return response                          # ③ 쿠키가 담긴 응답 반환
```

### 쿠키 읽기

```python
# 브라우저가 보낸 쿠키는 request에서 읽는다
value = request.COOKIES.get('my_cookie')
```

> **한 줄 요약**: 쿠키를 **설정**할 때는 Response, **읽을** 때는 `request.COOKIES`.

---

## 10. 쿠키 보안 속성

### `httponly` — XSS(Cross-Site Scripting) 방어

`httponly=True`로 설정된 쿠키는 JavaScript의 `document.cookie`로 **접근 불가**하다.
악성 스크립트가 페이지에 주입되더라도 쿠키를 훔쳐갈 수 없다.

```javascript
// httponly=True인 쿠키는 아래 코드로 볼 수 없음
console.log(document.cookie);  // my_cookie가 출력되지 않음
```

> **한 줄 요약**: 세션 ID나 인증 토큰이 담긴 쿠키는 반드시 `httponly=True`.

---

### `samesite` — CSRF(Cross-Site Request Forgery) 방어

외부 사이트(evil.com)에서 내 사이트(myapp.com)로 요청을 보낼 때 쿠키를 함께 전송할지 제어한다.

| 값 | 동작 | 권장 상황 |
|----|------|---------|
| `'Lax'` (기본값) | 링크 클릭(GET)은 허용, 외부 사이트의 POST 폼은 차단 | 일반적인 서비스 |
| `'Strict'` | 오직 같은 사이트 요청에만 쿠키 전송 | 보안이 최우선인 서비스 |
| `'None'` | 제한 없음 (반드시 `secure=True`와 함께 사용) | 크로스 도메인 필요 시 |

> **한 줄 요약**: `'Lax'`가 보안과 사용성의 균형점이다.

---

### `secure` — HTTPS 전용

| 값 | 동작 |
|----|------|
| `secure=False` | HTTP에서도 쿠키 전송 (개발 환경에서만 사용) |
| `secure=True` | HTTPS 연결에서만 쿠키 전송 (프로덕션 필수) |

---

## 11. `delete_cookie()`의 원리

**HTTP에는 "쿠키 삭제" 명령이 없다.**
`delete_cookie('name')`은 내부적으로 `set_cookie(key, max_age=0, expires=과거날짜)`를 호출해서 브라우저가 "이미 만료된 쿠키"로 인식하게 만드는 방식으로 삭제를 구현한다.

> **한 줄 요약**: 쿠키 삭제 = 만료 시간을 과거로 덮어씌우기.

---

## 12. 세션 vs 쿠키 최종 비교표

| 구분 | 세션 (Session) | 쿠키 (Cookie) |
|------|---------------|--------------|
| **저장 위치** | 서버 (DB / Cache / File) | 브라우저 |
| **브라우저 전송** | `sessionid` 쿠키 값만 전송 | 데이터 자체를 매 요청마다 전송 |
| **용량 제한** | 서버 용량에 따름 | 도메인당 약 4KB |
| **보안** | 높음 (데이터가 서버에 보관됨) | 낮음 (위변조 주의) |
| **데이터 쓰기** | `request.session['key'] = val` | `response.set_cookie(key, val)` |
| **데이터 읽기** | `request.session.get('key')` | `request.COOKIES.get('key')` |
| **데이터 삭제** | `del session['key']` / `flush()` | `response.delete_cookie('key')` |

### 언제 무엇을 쓸까?

```
세션을 쓰세요  →  로그인 상태, 장바구니, 민감한 사용자 데이터
쿠키를 쓰세요  →  테마/언어 설정, 팝업 "오늘 하루 안 보기", 간단한 추적 정보
```

---

## 13. 흔한 실수 모음

| 실수 | 원인 | 해결책 |
|------|------|--------|
| `session['key']` → `KeyError` 발생 | 키가 없을 때 직접 접근 | `session.get('key')` 사용 |
| mutable 객체 변경이 저장 안 됨 | Django가 내부 변경을 자동 감지 못함 | `session.modified = True` 수동 설정 |
| `set_expiry()`를 index 뷰에서 호출 | 매 요청마다 타이머가 리셋됨 | 세션 **생성** 뷰에서만 호출 |
| 쿠키가 브라우저에 전송 안 됨 | `request.set_cookie(...)` 시도 | `response` 객체에 설정 후 `return response` |
| 로그아웃 후 세션 재사용 가능 | `del`로만 삭제해 `sessionid`가 유지됨 | `session.flush()`로 세션 ID까지 교체 |