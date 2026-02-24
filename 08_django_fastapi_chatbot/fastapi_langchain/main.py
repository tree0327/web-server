from fastapi import FastAPI  # FastAPI 애플리케이션 객체 사용
from fastapi.middleware.cors import CORSMiddleware  # CORS 미들웨어 사용
from routers import chat_router  # 채팅 라우터 모듈
import uvicorn  # ASGI 서버 실행 도구

# FastAPI 앱 생성
app = FastAPI(
    title="ChatBot LangChain API",
    description="LangChain과 OpenAI를 연동한 챗봇용 FastAPI 서비스",
    version="1.0.0"  # API 버전 정보
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],  # Django 앱 주소 허용
    allow_credentials=True,  # 쿠키/인증 정보 포함 허용
    allow_methods=["*"],     # 모든 HTTP 메서드 허용
    allow_headers=["*"],     # 모든 헤더 허용
)

# 라우터 등록
app.include_router(chat_router.router, prefix="/chat", tags=["chat"])  # /chat 경로로 채팅 라우터 연결

# 기본 루트 경로 응답 함수
@app.get("/")
async def root():
    """루트 경로 접속 시 기본 정보를 반환한다."""
    return {
        "message": "ChatBot LangChain API가 실행 중입니다!",
        "version": "1.0.0",
        "docs": "/docs"  # Swagger 문서 경로
    }

# 서버 상태를 확인하는 헬스 체크 함수
@app.get("/health")
async def health_check():
    """서버의 정상 동작 여부를 반환한다."""
    return {"status": "healthy"}

# 현재 파일이 직접 실행할 때 Uvicorn 서버를 시작하는 코드
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)