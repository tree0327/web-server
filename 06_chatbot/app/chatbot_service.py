from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # 프롬프트템플릿, 대화이력 placeholder
from langchain.chat_models import init_chat_model  # 채팅 모델 로드
from langchain_core.runnables.history import RunnableWithMessageHistory  # 대화 이력 결합용
from langchain_core.chat_history import BaseChatMessageHistory  # 채팅 이력 기본 클래스
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage  # Langchain 메시지 타입

from dotenv import load_dotenv  # .env 환경변수 로드 함수
import os  # 운영체제 환경변수 처리

from .models import ChatMessage  # 채팅 메시지 DB 모델

load_dotenv()  # .env파일을 읽어 환경변수로 등록

class DatabaseChatMessageHistory(BaseChatMessageHistory):
    """데이터베이스 기반 채팅메시지 히스토리 객체"""
    def __init__(self, session_id):
        self.session_id = session_id  # 현재 대화 세션 ID 저장
    
    @property  # 메소드를 필드처럼 사용, 접근 시마다 메소드 호출
    def messages(self):
        """데이터베이스의 해당 세션의 대화내역을 로드"""
        chat_messages: list[ChatMessage] = ChatMessage.objects.filter(session_id = self.session_id)  # 해당 세션의 대화 내역 조회

        messages = []
        for chat_message in chat_messages:
            if chat_message.message_type == 'human':
                messages.append(HumanMessage(content=chat_message.content))  # 사용자 메시지로 변환
            else:
                messages.append(AIMessage(content=chat_message.content))     # AI 메시지로 변환
        
        return messages  # Langchain 메시지 목록 형태로 반환

    # Langchain 메시지를 데이터베이스 저장하는 함수
    def add_message(self, message: BaseMessage):
        # langchain message 객체 타입에 따라 model 객체로 변환 후 저장
        if isinstance(message, HumanMessage):
            message_type = 'human'  # 사용자 메시지 타입
        else:
            message_type = 'ai'  # AI 메시지 타입
        
        ChatMessage.objects.create(
            session_id = self.session_id,  # 현재 세션 ID
            message_type = message_type,   # 메시지 타입
            content = message.content      # 메시지 내용
        )
    
    # 현재 세션의 전체 대화 이력을 삭제하는 함수
    def clear(self):
        ChatMessage.objects.filter(session_id=self.session_id).delete()

prompt = ChatPromptTemplate.from_messages([
    ('system', '넌 IT 분야의 직업상담사 챗봇이야.'),  # 시스템 프롬프트
    MessagesPlaceholder(variable_name='history'),   # 이전 대화 이력을 삽입할 자리
    ('human', '{query}')  # 현재 사용자의 질문
])

# session_id를 받아 DB 기반 대화 이력 객체를 반환하는 함수
def get_by_session_id(session_id):
    return DatabaseChatMessageHistory(session_id)  # 세션별 히스토리 객체 생성

llm = init_chat_model('gpt-4.1-mini', temperature=0.7)  # 채팅 모델 초기화
chain = prompt | llm  # 프롬프트 + LLM 체인

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history = get_by_session_id,  # 세션별 이력 조회 함수
    input_messages_key = 'query',      # 사용자 입력 키
    history_messages_key = 'history'   # 대화 이력 키
)

# 세션별 대화 이력을 포함해 체인을 실행하는 함수
def invoke_chain_with_history(session_id, query):
    return chain_with_history.invoke({
        'query': query    # 현재 사용자 질문
    }, config = {
        'configurable': {
            'session_id': session_id  # 어떤 세션의 이력을 사용할지 지정
        }
    })