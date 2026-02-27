import boto3
from botocore.exceptions import NoCredentialsError  # 인증정보 예외 처리용
from django.conf import settings  # settings.py
from datetime import datetime     # 현재 날짜/시간 처리

class S3Client():
    # S3 클라이언트 생성 및 버킷명 초기화
    def __init__(self):
        self.s3 = boto3.client(
            's3',  # S3 서비스 클라이언트 생성
            aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
            region_name = settings.AWS_S3_REGION_NAME
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    
    # 전달받은 파일을 S3에 업로드하고, 업로드 된 파일 URL을 반환하는 함수
    def upload(self, file):
        save_dir = 'uploads/'  # S3 버킷 내 저장될 폴더
        now = datetime.now()
        date_prefix = now.strftime('%Y%m%d_%H%M%S_')  # 파일명 앞에 붙일 날짜/시간
        new_file_name = f"{date_prefix}{file.name}"   # 파일명 중복 방지용 새 이름
        extra_args = {'ContentType': file.content_type}  # 업로드 파일의 MIME 타입 정보

        try:
            self.s3.upload_fileobj(
                file,  # 업로드할 파일 객체
                self.bucket_name,  # 대상 S3 버킷명
                f'{save_dir}{new_file_name}',  # 저장될 경로
                ExtraArgs = extra_args  # 업로드 옵션
            )
            return f'https://{self.bucket_name}.s3.amazonaws.com/{save_dir}{new_file_name}'
        except NoCredentialsError:
            print('AWS 인증정보가 없습니다!!!!!')