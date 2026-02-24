import json  # JSON 데이터 처리
import requests  # FastAPI 서버로 HTTP 요청 전송
from django.shortcuts import render   # 템플릿 렌더링
from django.http import JsonResponse  # JSON 응답 객체
from django.views.decorators.csrf import csrf_exempt  # CSRF 검사 예외 처리
from django.conf import settings  # Django settings.py 설정값
from .models import ChatMessage   # 채팅 메시지 모델

def chat_view(request):
    """채팅 메인 화면을 렌더링해서 반환하는 함수"""
    session_id = request.GET.get('session_id')  # url 쿼리에서 세션 ID 조회

    context = {}
    if session_id:
        context = {'session_id': session_id}  # 세션 ID가 있으면 템플릿에 전달
    
    return render(request, 'chat/chat.html', context)

@csrf_exempt
def send_message(request):
    """사용자 메시지를 FastAPI 서비스로 보내고 응답을 반환하는 함수"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # 요청 본문 JSON 파싱
            user_message = data.get('message', '')  # 사용자 메시지 추출
            session_id = data.get('session_id', 'default')  # 세션 ID 추출
        
            if not user_message:
                return JsonResponse({'error': '메시지는 필수입니다'}, status=400)
            
            # FastAPI 서비스로 요청 전송
            fastapi_url = f"{settings.FASTAPI_SERVICE_URL}/chat/"
            payload = {
                'message': user_message,
                'session_id': session_id
            }

            response = requests.post(fastapi_url, json=payload, timeout=30)  # FastAPI 로 POST 요청

            if response.status_code == 200:
                bot_response = response.json().get('response', '')  # AI 응답 추출
            
                # 사용자 메시지 DB로 저장
                ChatMessage.objects.create(
                    session_id = session_id,
                    message_type = 'human',
                    content = user_message
                )

                # AI 응답 메시지 DB로 저장
                ChatMessage.objects.create(
                    session_id = session_id,
                    message_type = 'ai',
                    content = bot_response
                )

                return JsonResponse({
                    'response': bot_response,
                    'status': 'success'
                })
            
            else:
                return JsonResponse({
                    'error': 'FastAPI 서비스 오류',
                    'status': 'error'
                }, status=500)

        except requests.exceptions.RequestException as e:
            return JsonResponse({
                'error': f"연결 오류: {str(e)}",
                'status': 'error'
            }, status=500)
        except json.JSONDecodeError:
            return JsonResponse({'error': "잘못된 JSON 형식입니다."}, status=400)
        except Exception as e:
            return JsonResponse({
                'error': f"내부 오류: {str(e)}",
                'status': 'error'
            }, status=500)

    return JsonResponse({'error': 'POST 메서드만 허용됩니다!'}, status=405)


def get_history():
    """지정한 세션의 대화 이력을 조회해서 반환하는 함수"""
    session_id = requests.GET.get('session_id', 'default')  # 조회할 세션 ID
    messages = ChatMessage.objects.filter(session_id = session_id)[:20]  # 최근 20개 메시지 조회

    history = []  # 화면에 표시할 이력 목록
    service_history = []  # FastAPI 서비스 전달용 이력 목록
    for msg in messages:

        message_type = 'user' if msg.message_type == 'human' else 'bot'

        history.append({
            'type': message_type,    # user/bot 구분
            'message': msg.content,  # 메시지 내용
            'timestamp': msg.created_at.isoformat()  # 생성 시간 문자열 반환
        })

        # FastAPI 서비스에 전달할 LangChain 형식 이력 구성
        service_history.append({
            'type': 'human' if msg.message_type == 'human' else 'ai',  # LangChain용 타입 변환
            'content': msg.content
        })
    
    # FastAPI LangChain 세션에 이력을 넣어 이어 대화 가능하게 처리
    try:
        set_url = f"{settings.FASTAPI_SERVICE_URL}/chat/history/set"  # 이력 설정 엔드포인트 주소
        set_payload = {
            'session_id': session_id,
            'history': service_history
        }

        requests.post(set_url, json=set_payload, timeout=15)  # FastAPI 로 이력 동기화 요청
    
    except requests.exceptions.RequestException:
        pass  # 이력 동기화 실패시 무시 처리

    return JsonResponse({'history': history})  # 화면에 표시할 이력 반환