import uuid  # 고유한 세션 ID 생성 모듈
import json  # JSON 데이터 파싱 모듈
from django.views.decorators.csrf import csrf_exempt  # CSFR 검증 비활성화 데코레이터
from django.views.decorators.http import require_GET, require_POST, require_http_methods  # HTTP 메서드 제한 데코레이터
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, Http404  # JSON 응답, 오류 응답 처리
from django.shortcuts import render  # 템플릿 렌더링 함수
from .models import ChatMessage  # 채팅 메시지 모델
from .chatbot_service import get_by_session_id, invoke_chain_with_history  # 세션별 대화 이력, 체인 호출 함수

# 메인 페이지 렌더링하는 함수
def index(request):
    return render(request, 'app/index.html')

# 새 대화에 사용할 고유한 session_id를 생성하는 함수
@csrf_exempt   # csrf 토큰인증 비활성화
@require_POST
def init_conversation(request):
    session_id = str(uuid.uuid4())  # uuid 기반 고유 세션 ID 생성
    return JsonResponse({
        'session_id': session_id
    })

# 사용자의 질문을 받아 대화 이력을 포함한 챗봇 응답을 반환하는 함수
@csrf_exempt
@require_POST
def chatbot(request):
    session_id = request.POST.get('session_id')  # 요청 데이터에서 session_id 추출
    print(session_id)
    query = request.POST.get('query')  # 사용자 질문 추출

    # 유효성 검사 : 필수값 누락시 400에러
    if not session_id or not query:
        return HttpResponseBadRequest('세션ID나 질문은 필수입니다!')
    
    response = invoke_chain_with_history(session_id, query)  # 대화 이력 반영한 챗봇 호출
    return JsonResponse({
        'content': response.content
    })

# 특정 세션의 대화 이력을 삭제하는 함수
@csrf_exempt
@require_http_methods(['DELETE'])  # 요청 메소드가 DELETE
def remove_conversation(request):
    try:
        body = json.loads(request.body)      # JSON 문자열 -> python dict/list로 변환
        session_id = body.get('session_id')  # 삭제할 session_id 추출
    except json.JSONDecodeError:
        return HttpResponseBadRequest('JSON body를 식별할 수 없습니다.')  # JSON 형식 오류 발생시 400 에러 응답
    
    # 해당 세션 ID를 ChatMessage 모델 객체에서 찾지 못하면 404 에러 응답
    if not ChatMessage.objects.filter(session_id=session_id).exists():
        raise Http404('세션 ID를 찾지 못하였습니다.')
    
    # DB에서 삭제
    history = get_by_session_id(session_id)  # 세션별 대화 이력 객체 조회
    history.clear()  # 해당 세션의 대화 이력 전체 삭제

    return JsonResponse({
        'result': 'success',
        'message': f'세션 ID {session_id}의 대화이력 삭제 완료!'
    })

# 저장된 대화 세션 목록을 집계해서 반환하는 함수
@require_GET
def get_session_list(request):
    from django.db.models import Min, Max, Count  # 집계 함수

    sessions = ChatMessage.objects.values('session_id').annotate(
        first_message_time = Min('created_at'),  # 세션별 첫 메시지 시간
        last_message_time = Max('created_at'),   # 세션별 마지막 메시지 시간
        message_count = Count('id')              # 세션별 메시지 갯수
    )
    print(sessions)

    session_list = []
    for session in sessions:
        first_message = ChatMessage.objects.filter(session_id=session['session_id']).first()  # 각 세션의 첫 메시지 조회

        session_list.append({
            'session_id': session['session_id'],
            'first_message_preview': first_message.content,
        })
    
    return JsonResponse({
        'sessions': session_list,  # 세션 목록
        'total_sessions': len(session_list)  # 전체 세션 갯수
    })

# 저장된 세션의 대화 내용을 다시 불러오는 함수
@csrf_exempt
@require_POST
def restore_conversation(request):
    try:
        body = json.loads(request.body)      # JSON 문자열 -> python dict/list로 변환
        session_id = body.get('session_id')  # 복원할 session_id 추출
    except json.JSONDecodeError:
        return HttpResponseBadRequest('JSON body를 식별할 수 없습니다.')  # JSON 형식 오류 발생시 400 에러 응답
    
    # 해당 세션 ID를 ChatMessage 모델 객체에서 찾지 못하면 404 에러 응답
    if not ChatMessage.objects.filter(session_id=session_id).exists():
        # == raise Http404('세션 ID를 찾지 못하였습니다.')
        return HttpResponseNotFound('세션ID를 찾지 못하였습니다.')
    
    history = get_by_session_id(session_id)  # 세션별 대화 이력 객체 조회
    conversation_history = []
    for message in history.messages:
        conversation_history.append({
            'type': message.type,        # 메시지 유형
            'content': message.content   # 메시지 내용
        })

    return JsonResponse({
        'session_id': session_id,  # 복원한 세션 ID
        'conversation_history': conversation_history,  # 전체 대화 이력
        'message_count': len(conversation_history)     # 메시지 갯수
    })