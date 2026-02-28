from django.db import models  # Django Model 기능
from django import forms      # Django Form 기능

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')  # 업로드 파일을 uploads/ 경로를 기준으로 저장
    uploaded_at = models.DateTimeField(auto_now_add=True)  # 파일 업로드 시간 자동 저장

    # 파일 객체를 문자열로 확인시
    def __str__(self):
        return self.file.name  # 파일 이름 반환

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile  # UploadedFile 모델 기반 폼 생성
        fields = ['file']     # 폼에 포함될 필드