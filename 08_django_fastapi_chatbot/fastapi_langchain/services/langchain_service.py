import os
from typing import Dict, List, Optional  # 타입 힌트 작성
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # 프롬프트 템플릿 구성
from langchain_core.runnables.history import RunnableWithMessageHistory  # 대화 이력 포함 실행 객체
from langchain_core.chat_history import InMemoryChatMessageHistory    # 메모리 기반 대화 이력 저장소
from langchain_core.chat_history import BaseChatMessageHistory    # 대화 이력 기본 타입
import logging  # 로그 출력 기능

# 환경변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO)  # INFO 레벨 이상 로그 출력
logger = logging.getLogger(__name__)     # 현재 모듈 로거 생성

class LangChainChatService:
    """RunnableWithMessageHistory를 사용한 LangChain 채팅 서비스 클래스"""
    
    def __init__(self):
        """OpenAI 설정과 체인을 초기화"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY 환경변수가 필요합니다!")
        
        self.model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
        
        # OpenAI 채팅 모델 초기화
        self.llm = ChatOpenAI(
            api_key=self.api_key,                  # OpenAI API 키
            model=self.model_name,                 # 사용할 모델
            temperature=self.temperature,          # 응답 창의성
            max_completion_tokens=self.max_tokens  # 최대 생성 토큰
        )
        
        # 대화 이력 자리를 포함한 프롬프트 템플릿 생성
        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system", 
                "You are a helpful AI assistant. You provide clear, accurate, and helpful responses. "
                "You can communicate in Korean or English based on the user's preference. "
                "Be conversational and friendly."
            ),  # 시스템 프롬프트
            MessagesPlaceholder(variable_name="history"),  # 이전 대화 이력 추가될 위치
            ("human", "{input}")  # 사용자 입력값
        ])
        
        # 프롬프트와 모델을 연결해 체인 구성
        self.chain = self.prompt | self.llm
        
        # 세션별 대화 이력 저장소
        self.session_stores: Dict[str, InMemoryChatMessageHistory] = {}  # 세션별 메모리 저장 초기화
        
        # 대화 이력을 포함한 실행 객체 생성
        self.runnable_with_history = RunnableWithMessageHistory(
            self.chain,  # 실행할 체인
            self.get_session_history,        # 세션 이력 조회 함수
            input_messages_key="input",      # 입력 메시지 키 이름
            history_messages_key="history",  # 이력 메시지 키 이름
        )
        
        logger.info(f"LangChain 서비스 초기화 완료 - 모델: {self.model_name}")
    
    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """세션에 해당하는 대화 이력을 반환"""
        if session_id not in self.session_stores:
            self.session_stores[session_id] = InMemoryChatMessageHistory()  # 새 세션 이력 생성
            logger.info(f"세션 대화 이력 새로 생성: {session_id}")
        
        return self.session_stores[session_id]  # 해당 세션 대화 이력 반환
    
    async def get_chat_response(self, message: str, session_id: str = "default") -> str:
        """세션 이력을 반영해 AI 응답을 생성하는 비동기 함수"""
        try:
            logger.info(f"세션 {session_id}의 OpenAI 요청 메시지 미리보기: {message[:50]}...")
            
            # RunnableWithMessageHistory를 사용한 응답 생성
            response = await self.runnable_with_history.ainvoke(
                {"input": message},  # 사용자 입력
                config={"configurable": {"session_id": session_id}}  # 세션 ID 설정
            )
            
            bot_response = response.content  # 응답 본문 추출
            logger.info(f"세션 {session_id}의 응답 수신 미리보기: {bot_response[:50]}...")
            
            return bot_response
            
        except Exception as e:
            logger.error(f"채팅 응답 생성 중 오류 발생: {str(e)}")
            raise Exception(f"AI 응답 생성 실패: {str(e)}")
    
    def clear_session_memory(self, session_id: str) -> bool:
        """지정한 세션의 대화 메모리를 삭제"""
        if session_id in self.session_stores:
            del self.session_stores[session_id]  # 세션 이력 삭제
            logger.info(f"세션 대화 이력 삭제 완료: {session_id}")
            return True  # 삭제 성공
        return False  # 삭제할 세션 없음
    
    def get_chat_history_for_display(self, session_id: str) -> List[Dict]:
        """세션의 대화 이력을 화면 표시 형식으로 반환"""
        if session_id not in self.session_stores:
            return []  # 세션 없으면 빈 리스트
        
        chat_history = self.session_stores[session_id]  # 세션 대화 이력 조회
        messages = chat_history.messages  # 저장된 메시지 목록
        
        history = []
        for msg in messages:
            if hasattr(msg, 'type'):
                if msg.type == "human":
                    history.append({"type": "user", "content": msg.content})
                elif msg.type == "ai":
                    history.append({"type": "assistant", "content": msg.content})
        
        return history
    
    def get_active_sessions(self) -> List[str]:
        """현재 저장된 세션 ID 목록을 반환"""
        return list(self.session_stores.keys())  # 세션 ID 리스트

    def set_history(self, session_id: str, items: List[Dict[str, str]]) -> int:
        """전달받은 대화 목록으로 세션 이력을 새로 설정"""
        # 대화 이력 초기화
        self.session_stores[session_id] = InMemoryChatMessageHistory()
        loaded = 0   # 저장된 메시지 숫자

        for item in items:
            try:
                message_type = (item.get("type") or "").lower()  # 메시지 타입 소문자 처리
                content = item.get("content") or ""  # 메시지 내용
                if not content:
                    continue   # 내용이 없으면 건너뜀
                if message_type in ("human", "user"):
                    self.session_stores[session_id].add_user_message(content)  # 사용자 메시지 저장소에 저장
                    loaded += 1
                elif message_type in ("ai", "assistant"):
                    self.session_stores[session_id].add_ai_message(content)  # AI 메시지 저장소에 저장
                    loaded += 1
            except Exception as e:
                logger.warning(f"세션 {session_id}의 잘못된 이력 항목 건너뜀: {e}")
        logger.info(f"세션 {session_id}의 {loaded}개의 이력 메시지 저장 완료")
        return loaded
    
# 전역 채팅 서비스 인스턴스 설정
chat_service = LangChainChatService() 