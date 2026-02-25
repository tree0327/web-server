from django.contrib import admin
from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """ChatMessage 모델의 관리자 페이지 설정"""
    
    list_display = ['id', 'session_id', 'message_type', 'content_preview', 'created_at']  # 표시할 컬럼
    list_filter = ['session_id', 'message_type', 'created_at']  # 우측에 필터 적용할 항목들
    search_fields = ['content', 'session_id']  # 검색 가능한 필드
    readonly_fields = ['created_at']  # 수정 불가능한 필드
    ordering = ['-created_at']  # 최신순 정렬
    
    def content_preview(self, obj):
        """메시지 내용을 50자 기준으로 잘라 미리보기로 반환"""
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Message Content'  # 관리자 페이지 컬럼명
    
    def has_add_permission(self, request):
        """관리자 페이지에서 직접 메시지를 추가하지 못하게 함"""
        return False
    
    def get_queryset(self, request):
        """관리자 페이지에서 사용할 조회 객체 반환"""
        return super().get_queryset(request).select_related()  # 연관 객체 조회