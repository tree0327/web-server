from django.contrib import messages  # 사용자 알림 메시지 프레임워크
from django.shortcuts import render, redirect  # 템플릿 응답, 페이지 이동

from .aws_s3_service import S3Client  # S3 업로드 처리 클래스
from .models import FileUploadForm    # 파일 업로드하는 폼

s3_client = S3Client()  # S3 업로드용 클라이언트 객체

# 업로드 된 파일을 S3에 저장하고, 결과를 화면에 반환하는 함수
def upload_file(request):
    """GET 요청이면 업로드 폼 출력, POST요청이면 파일 업로드 & DB 저장"""
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)  # 일반 데이터와 파일 데이터를 함께 폼에 바인딩
        print(form.__dict__)

        if form.is_valid():
            model = form.save(commit=False)  # 모델 객체 생성(DB 저장 X)
            print(model.file)  # 파일 필드 정보
            obj_url = s3_client.upload(form.files['file'])  # 전송된 파일을 S3에 업로드하고 URL을 반환
            print(obj_url)
            model.file = obj_url  # S3 URL을 모델 file 필드에 저장
            model.save()  # 모델 객체를 DB 반영
            messages.success(request, """
            파일 업로드가 성공하였습니다!
            <a href="{obj_url}">업로드된 파일 확인</a>을 눌러 확인해주세요!!
            """.format(obj_url=obj_url))
            return redirect('app:upload')  # 업로드 페이지로 다시 이동
    else:
        form = FileUploadForm()  # GET 요청시에는 빈 업로드 폼 생성
    
    return render(request, 'app/upload.html', {'form': form})
