from django.db import models

class ChatMessage(models.Model):
    """메시지 내역을 저장하는 모델"""
    session_id = models.CharField(max_length=255, db_index=True)  # 대화 세션 ID : 최대 255. 인덱스 사용하여 검색 성능 향상
    message_type = models.CharField(max_length=10, choices=[
        ('human', 'Human'),  # 사용자 메시지 타입
        ('ai', 'AI')         # AI 메시지 타입
    ])
    content = models.TextField()  # 메시지 본문 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 메시지 생성 시간 (자동저장)

    # 관리자나 디버깅 시 메시지 객체를 문자열로 보기 좋게 표현하는 함수
    def __str__(self):
        return f'{self.session_id} - {self.message_type}: {self.content[:50]}...'  # 세션 ID, 타입, 앞부분 내용
    
    class Meta:
        ordering = ['created_at']  # 메시지는 생성 시각 오름차순으로 정렬