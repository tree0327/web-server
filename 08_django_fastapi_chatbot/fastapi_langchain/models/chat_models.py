from pydantic import BaseModel, Field  # Pydantic 모델과 필드 옵션
from typing import Optional    # 선택적으로 값이 들어올 수 있는 타입
from datetime import datetime  # 현재 시각

class ChatRequest(BaseModel):
    """채팅 요청 데이터 모델"""
    message: str = Field(..., description="User message", min_length=1, max_length=2000)  # 사용자가 입력한 메시지
    session_id: Optional[str] = Field(default="default", description="Session identifier")  # 대화 구분용 세션 ID

class ChatResponse(BaseModel):
    """채팅 응답 데이터 모델"""
    response: str = Field(..., description="Bot response message")  # 챗봇이 반환하는 응답
    session_id: str = Field(..., description="Session identifier")  # 응답이 속한 세션 ID
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp") # 응답 생성 시간

class ErrorResponse(BaseModel):
    """에러 응답 데이터 모델"""
    error: str = Field(..., description="Error message")  # 에러 메시지
    detail: Optional[str] = Field(None, description="Detailed error information")  # 에러 상세내용

class HealthResponse(BaseModel):
    """서버 상태 확인용 응답 모델"""
    status: str = Field(..., description="Service status")  # 현재 서비스 상태
    timestamp: datetime = Field(default_factory=datetime.now, description="Check timestamp")  # 상태 확인 시간

class HistoryItem(BaseModel):
    """세션에 저장할 단일 대화 이력 모델"""
    type: str = Field(..., description="Message type: 'human'|'user' or 'ai'|'assistant'")  # 메시지 작성 주체
    content: str = Field(..., description="Message content")  # 실제 대화 내용

class SetHistoryRequest(BaseModel):
    """세션 이력을 설정하기 위한 요청 데이터 모델"""
    session_id: Optional[str] = Field(default="default", description="Session identifier")  # 대화 이력 저장할 세션 ID
    history: list[HistoryItem] = Field(default_factory=list, description="Ordered list of messages to set for the session")  # 저장할 대화 이력 목록