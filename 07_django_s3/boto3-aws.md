# boto3 +AWS

## boto3 라이브러리

`boto3`는 Python에서 **AWS(Amazon Web Services) 리소스를 프로그래밍적으로 제어**할 수 있게 해주는 공식 SDK이다.
즉, Python 코드로 EC2 인스턴스를 생성하거나, S3 버킷을 관리하거나, DynamoDB에 데이터를 넣을 수 있다.

구조적으로는 크게 두 가지 인터페이스를 제공한다.

1. **Client 인터페이스** → 저수준 API 호출 (AWS API와 1:1 매핑됨)
2. **Resource 인터페이스** → 객체지향 스타일 API 제공 (좀 더 Pythonic하게 사용 가능)

---

### ⚙️ boto3로 제어 가능한 주요 AWS 서비스

boto3는 AWS의 대부분의 서비스와 연동된다. 아래는 대표적인 서비스 목록이다.

#### 🗄️ 스토리지

* **S3 (Simple Storage Service)** : 객체 스토리지 (파일 업로드/다운로드, 버킷 관리)
* **EFS (Elastic File System)** : 확장 가능한 네트워크 파일 스토리지
* **Glacier** : 장기 아카이브 스토리지

#### 💻 컴퓨팅

* **EC2 (Elastic Compute Cloud)** : 가상 서버 인스턴스 생성/중지/삭제
* **Lambda** : 서버리스 함수 실행 제어
* **ECS / EKS** : 컨테이너 오케스트레이션 (Docker, Kubernetes)

#### 🗂️ 데이터베이스

* **DynamoDB** : NoSQL 데이터베이스
* **RDS (Relational Database Service)** : MySQL, PostgreSQL, MariaDB, Oracle, SQL Server 관리
* **Aurora** : AWS 고성능 관계형 DB

#### 📡 네트워크 & 보안

* **VPC (Virtual Private Cloud)** : 네트워크 관리
* **Route53** : DNS 관리
* **IAM (Identity and Access Management)** : 사용자/역할/정책 관리
* **KMS (Key Management Service)** : 암호화 키 관리

#### 📊 데이터 분석 & 메시징

* **SQS (Simple Queue Service)** : 메시지 큐 관리
* **SNS (Simple Notification Service)** : 알림/메시징 서비스
* **Kinesis** : 스트리밍 데이터 처리
* **Athena** : S3 데이터를 SQL로 조회

#### 🤖 머신러닝 & AI

* **SageMaker** : 머신러닝 모델 학습/배포
* **Rekognition** : 이미지/영상 분석
* **Polly** : 텍스트 음성 변환
* **Comprehend** : 자연어 처리 (감정 분석, 키워드 추출)

#### 🔧 기타 주요 서비스

* **CloudFormation** : 인프라 코드(IaC) 관리
* **CloudWatch** : 로그/모니터링
* **Step Functions** : 워크플로우 오케스트레이션
* **CodeCommit / CodeBuild / CodeDeploy / CodePipeline** : CI/CD 파이프라인