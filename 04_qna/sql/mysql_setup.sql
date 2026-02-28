# root 관리자 실행

-- qnadb 데이터베이스를 utf8mb4 문자셋으로 생성
create database qnadb character set utf8mb4 collate utf8mb4_unicode_ci;

-- django 계정에 qnadb의 모든 권한 부여
grant all privileges on qnadb.* to 'django'@'%';
flush privileges;  -- 권한 변경 사항 즉시 반영