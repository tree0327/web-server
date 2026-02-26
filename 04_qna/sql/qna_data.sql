use qnadb;

START TRANSACTION;
INSERT INTO qnadb.qna_question (id, subject, content, created_at, modified_at, author_id) VALUES (1, 'Django 캐치프레이즈 의미', 'The python web framework for perfectionists with deadlines. 이게 무슨 말인가요?', '2025-01-03 22:24:47.377130', '2025-01-07 04:56:33.037743', null);
INSERT INTO qnadb.qna_question (id, subject, content, created_at, modified_at, author_id) VALUES (2, 'Django의 특징 질문', '장고의 특징이 MTV 아키텍처, ORM, 자동 관리자 인터페이스, 보안 기능, 확장성, URL 라우팅, 템플릿 시스템이라는데, 이게 무슨 말인가요?', '2025-01-03 22:24:47.388293', '2025-01-07 04:56:33.037743', null);
INSERT INTO qnadb.qna_question (id, subject, content, created_at, modified_at, author_id) VALUES (3, 'ORM과 SQL Mapper 차이 설명 부탁드려요.🫰', '살려주세요ㅠ', '2025-01-03 22:24:47.395502', '2025-01-07 04:56:33.037743', null);
INSERT INTO qnadb.qna_question (id, subject, content, created_at, modified_at, author_id) VALUES (4, 'CSRF, XSS, SQL 인젝션ㅠ 이게 다 뭐요?', '장고가 제공하는 다양한 보안 기능을 알고 쓰고 싶어요~', '2025-01-03 22:24:47.402623', '2025-01-07 04:56:33.037743', null);
INSERT INTO qnadb.qna_question (id, subject, content, created_at, modified_at, author_id) VALUES (5, 'Django vs Spring', '대규모 프로젝트에서 적합한 프로젝트는 무엇일까요?', '2025-01-03 22:24:50.490134', '2025-01-07 04:56:33.037743', null);

INSERT INTO qnadb.qna_answer (id, content, created_at, modified_at, author_id, question_id) VALUES (1, 'deadline은 사선입니다.', '2025-01-05 01:17:13.289879', '2025-01-07 04:56:32.975927', null, 1);
INSERT INTO qnadb.qna_answer (id, content, created_at, modified_at, author_id, question_id) VALUES (2, 'chat gpt한테 물어보세요. 잘 알려줍니다~ 🤖', '2025-01-08 01:08:24.833848', '2025-01-07 04:56:32.975927', null, 2);
INSERT INTO qnadb.qna_answer (id, content, created_at, modified_at, author_id, question_id) VALUES (3, 'ORM(Object-Relational Mapping)이란 객체 지향 프로그래밍 언어를 사용해 데이터베이스의 데이터를 객체처럼 다룰 수 있도록 매핑해주는 도구이다. 라고 하네요. G선생님이... 😊😊😊', '2025-01-08 01:08:29.399623', '2025-01-07 04:56:32.975927', null, 2);
COMMIT;
ROLLBACK; # 위 DML 실행중 오류가 발생한 경우