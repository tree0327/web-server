from fastapi import APIRouter, HTTPException, Depends  # FastAPI 라우터, 예외처리 도구
from models.chat_models import ChatRequest, ChatResponse, ErrorResponse, SetHistoryRequest  # 요청/응답 데이터 모델
from services.langchain_service import chat_service  # 채팅 서비스 객체
import logging  # 로그 출력
from typing import List  # 리스트 타입 힌트

# 로깅 설정
logger = logging.getLogger(__name__)

# 라우터 생성
router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def send_message(chat_request: ChatRequest):
    """챗봇에게 메시지를 보내고 응답을 반환"""
    try:
        logger.info(f"세션 {chat_request.session_id}의 채팅 요청 수신하였습니다.")
        
        # LangChain 서비스로부터 응답 받기
        response = await chat_service.get_chat_response(
            message=chat_request.message,         # 사용자 메시지
            session_id=chat_request.session_id    # 세션 ID
        )
        
        return ChatResponse(
            response=response,  # 챗봇 응답 내용
            session_id=chat_request.session_id
        )
        
    except Exception as e:
        logger.error(f"채팅 요청 처리 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500,  # 서버 내부 오류 상태코드
            detail=f"채팅 요청 처리 실패: {str(e)}"
        )


@router.get("/history/{session_id}")
async def get_chat_history(session_id: str):
    """지정한 세션의, 대화 이력을 반환"""
    try:
        history = chat_service.get_chat_history_for_display(session_id)  # 화면 표시용 이력 조회
        return {"session_id": session_id, "history": history}
        
    except Exception as e:
        logger.error(f"대화 이력 조회 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"대화 이력 조회 실패: {str(e)}"
        )

@router.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """지정한 세션의 대화 이력을 삭제"""
    try:
        success = chat_service.clear_session_memory(session_id)  # 세션 이력 삭제 시도
        if success:
            return {"message": f"세션 {session_id} 삭제 완료"}
        else:
            return {"message": f"세션 {session_id}가 없거나 이미 비어 있음"}
            
    except Exception as e:
        logger.error(f"세션 삭제 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"세션 삭제 실패: {str(e)}"
        )

@router.get("/sessions")
async def list_active_sessions():
    """현재 활성화된 세션 목록을 반환"""
    try:
        sessions = chat_service.get_active_sessions()  # 활성 세션 목록 조회
        return {"active_sessions": sessions, "count": len(sessions)}  # 세션 목록과 개수
        
    except Exception as e:
        logger.error(f"세션 목록 조회 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"세션 목록 조회 실패: {str(e)}"
        )

@router.get("/test")
async def test_endpoint():
    """채팅 라우터가 정상적으로 동작하는 확인"""
    return {
        "message": "채팅 라우터가 정상적으로 동작 중입니다!",
        "service_status": "active"
    }


# 세션에 대화 이력을 직접 설정하는 엔드포인트
@router.post("/history/set")
async def set_history(request: SetHistoryRequest):
    try:
        session_id = request.session_id or "default"  # 세션 ID가 없으면 기본값 default
        print(f'{session_id=}, {request.history=}')
        # 요청 이력을 딕셔너리 목록으로 변환
        loaded = chat_service.set_history(session_id=session_id, items=[{"type": item.type, "content": item.content} for item in request.history])
        return {"message": "History set", "session_id": session_id, "loaded": loaded}
    except Exception as e:
        logger.error(f"대화 이력 설정 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"대화 이력 설정 실패: {str(e)}") 