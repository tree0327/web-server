from django.db import models
from django.utils import timezone  # 현재 시간 처리 도구

class ChatMessage(models.Model):
    """대화 메시지를 저장하는 모델"""
    MESSAGE_TYPE_CHOICES = [
        ('human', '사용자'),  # 사용자 메시지 타입
        ('ai', 'AI')         # AI 메시지 타입
    ]

    session_id = models.CharField(max_length=255, db_index=True)  # 최대 255자 세션 ID (인덱싱)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES)  # 최대 10자 메시지 유형 선택값
    content = models.TextField()  # 메시지 본문 내용
    created_at = models.DateTimeField(default=timezone.now)  # 메시지 생성 시간

    class Meta:
        ordering = ['created_at']  # 생성 시간 기준 오름차순 정렬
    
    def __str__(self):
        return f"{self.session_id} - {self.message_type}: {self.content[:50]}..."