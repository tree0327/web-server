import boto3  # AWS 서비스에 접근 라이브러리
import os
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError  # AWS 인증 정보 에러 처리용

# .env 파일 로드
load_dotenv()

"""
1. 설치 pip install boto3 python-dotenv
2. .env 파일에 IAM 사용자의 액세스 키와 비밀 액세스 키를 설정  
   AWS_ACCESS_KEY_ID=your_access_key_here
   AWS_SECRET_ACCESS_KEY=your_secret_key_here
   AWS_DEFAULT_REGION=ap-northeast-2
"""
AWS_ACCESS_KEY_ID=os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME=os.getenv('AWS_S3_REGION_NAME', 'ap-northeast-2')  # 기본값 설정
AWS_STORAGE_BUCKET_NAME=os.getenv('AWS_STORAGE_BUCKET_NAME')

s3 = boto3.client(
    's3',  # S3 서비스 클라이언트 생성
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_S3_REGION_NAME  # 기본값 설정
)
# 파일 업로드 예제
# s3client.upload_file(업로드할 파일명, 버킷명, 저장할 경로)

FILE_PATH = 'yes.gif'
UPLOAD_FILE_PATH = 'capy/ '

try:
    s3.upload_file(FILE_PATH, AWS_STORAGE_BUCKET_NAME, UPLOAD_FILE_PATH) # 반환값 없음

    # 아래 url중 하나 사용
    # file_url = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/{UPLOAD_FILE_PATH}"  # 리전 포함 URL
    file_url = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{UPLOAD_FILE_PATH}"  # 기본 S3 URL
    
    print(f"Upload Successful!: {file_url}")
except NoCredentialsError:
    print("Credentials not available")