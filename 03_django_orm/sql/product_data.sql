-- djangodb 데이터베이스 사용
use djangodb;

-- 트랜잭션 시작
START TRANSACTION;

-- 카테고리 데이터 입력
INSERT INTO djangodb.product_category (id, name) VALUES 
(1, '가전'),
(2, '스마트폰/태블릿'),
(3, '가구/인테리어'),
(4, '패션/의류'),
(5, '스포츠/레저'),
(6, '패션/액세서리');

-- 상품 데이터 입력
INSERT INTO djangodb.product_product (id, name, description, price, stock, available, created_at, updated_at) VALUES 
(1, 'iPhone 15 Pro', '애플의 최신 스마트폰, 강력한 A17 Pro 칩셋과 뛰어난 카메라 성능.', 1490000, 20, 1, CURRENT_TIMESTAMP - INTERVAL 19 DAY, CURRENT_TIMESTAMP - INTERVAL 19 DAY),
(2, 'Galaxy Z Flip5', '삼성의 폴더블 스마트폰, 컴팩트한 디자인과 혁신적인 힌지.', 1350000, 15, 1, CURRENT_TIMESTAMP - INTERVAL 19 DAY, CURRENT_TIMESTAMP - INTERVAL 19 DAY),
(3, 'LG 올레드 TV 55인치', '최상의 화질을 제공하는 LG 올레드 TV. 영화 감상에 최적화.', 1790000, 10, 1, CURRENT_TIMESTAMP - INTERVAL 19 DAY, CURRENT_TIMESTAMP - INTERVAL 19 DAY),
(4, 'Dyson V12 무선청소기', '다이슨의 최첨단 무선청소기. 강력한 흡입력과 긴 배터리 수명.', 899000, 25, 1, CURRENT_TIMESTAMP - INTERVAL 19 DAY, CURRENT_TIMESTAMP - INTERVAL 19 DAY),
(5, 'Nintendo Switch OLED 모델', '닌텐도의 인기 있는 게임 콘솔, 선명한 OLED 화면.', 419000, 30, 1, CURRENT_TIMESTAMP - INTERVAL 19 DAY, CURRENT_TIMESTAMP - INTERVAL 19 DAY),
(6, 'MacBook Air 15인치 M2', '애플의 초경량 노트북, M2 칩셋 탑재로 향상된 성능.', 1890000, 10, 1, CURRENT_TIMESTAMP - INTERVAL 19 DAY, CURRENT_TIMESTAMP - INTERVAL 19 DAY),
(7, 'Sony WH-1000XM5', '소니의 프리미엄 노이즈 캔슬링 헤드폰, 뛰어난 음질 제공.', 499000, 40, 1, CURRENT_TIMESTAMP - INTERVAL 19 DAY, CURRENT_TIMESTAMP - INTERVAL 19 DAY),
(8, 'Canon EOS R6 Mark II', '캐논의 풀프레임 미러리스 카메라, 프로급 사진 촬영에 적합.', 2790000, 5, 1, CURRENT_TIMESTAMP - INTERVAL 19 DAY, CURRENT_TIMESTAMP - INTERVAL 19 DAY),
(9, 'Apple Watch Series 9', '애플의 스마트워치, 더 밝은 디스플레이와 혁신적인 기능.', 599000, 50, 1, CURRENT_TIMESTAMP - INTERVAL 19 DAY, CURRENT_TIMESTAMP - INTERVAL 19 DAY),
(10, 'Samsung Bespoke 냉장고', '삼성의 맞춤형 디자인 냉장고, 고급스러운 인테리어 연출.', 2990000, 8, 1, CURRENT_TIMESTAMP - INTERVAL 19 DAY, CURRENT_TIMESTAMP - INTERVAL 19 DAY);

-- 상품-카테고리 다대다 관계 데이터 입력
INSERT INTO djangodb.product_category_product (id, category_id, product_id) VALUES 
(1, 1, 3),
(2, 1, 4),
(3, 1, 10),
(4, 2, 1),
(5, 2, 2),
(6, 2, 6),
(7, 2, 9),
(12, 3, 3),
(13, 3, 4),
(14, 3, 10),
(8, 5, 5),
(9, 5, 9),
(10, 6, 7),
(11, 6, 9);

-- 할인 정보 데이터 입력
INSERT INTO djangodb.product_discount (id, discount_percentage, start_date, end_date, product_id) VALUES
(1, 0.1, CURRENT_TIMESTAMP - INTERVAL 15 DAY, CURRENT_TIMESTAMP - INTERVAL 5 DAY, 3),
(2, 0.15, CURRENT_TIMESTAMP - INTERVAL 10 DAY, CURRENT_TIMESTAMP, 5),
(3, 0.2, CURRENT_TIMESTAMP + INTERVAL 12 DAY, CURRENT_TIMESTAMP + INTERVAL 21 DAY, 7),
(4, 0.5, CURRENT_TIMESTAMP - INTERVAL 8 DAY, CURRENT_TIMESTAMP - INTERVAL 2 DAY, 8),
(5, 0.25, CURRENT_TIMESTAMP - INTERVAL 5 DAY, CURRENT_TIMESTAMP + INTERVAL 5 DAY, 10);

-- 리뷰 데이터 입력
INSERT INTO djangodb.product_review (id, user_id, rating, comment, created_at, product_id) VALUES 
(1, 1, 5, '살짝 무겁긴 한데, 간지가 장난 아닙니다.', CURRENT_TIMESTAMP - INTERVAL 19 DAY, 1),
(2, 2, 4, '카메라 성능은 최고! 하지만 발열이 좀 있네요.', CURRENT_TIMESTAMP - INTERVAL 18 DAY, 1),
(3, 10, 5, '사진 퀄리티가 대단합니다. 프로급 장비 같아요.', CURRENT_TIMESTAMP - INTERVAL 17 DAY, 1),
(4, 11, 2, '이번 모델은 아쉽네요. 이전 모델이 더 좋았어요ㅠ', CURRENT_TIMESTAMP - INTERVAL 16 DAY, 1),
(5, 3, 5, '폴더블이라 휴대성 짱! 힌지가 정말 부드럽습니다.', CURRENT_TIMESTAMP - INTERVAL 18 DAY, 2),
(6, 4, 3, '디자인은 예쁜데, 배터리가 빨리 닳아요.', CURRENT_TIMESTAMP - INTERVAL 17 DAY, 2),
(7, 5, 5, '올레드 화질은 정말 최고입니다. 영화 볼 때 몰입감이 대단하네요.', CURRENT_TIMESTAMP - INTERVAL 17 DAY, 3),
(8, 6, 4, '흡입력은 강력하지만 무게가 조금 무겁습니다.', CURRENT_TIMESTAMP - INTERVAL 16 DAY, 4),
(9, 7, 5, '다이슨 청소기 중 가장 만족스러운 모델이에요!', CURRENT_TIMESTAMP - INTERVAL 15 DAY, 4),
(10, 8, 5, 'OLED 화면 너무 선명하고, 게임 플레이하기에 딱이에요!', CURRENT_TIMESTAMP - INTERVAL 14 DAY, 5),
(11, 9, 4, '휴대 모드가 편리하고 화면도 좋아요.', CURRENT_TIMESTAMP - INTERVAL 13 DAY, 5),
(12, 10, 5, '닌텐도 팬으로서 너무 만족스럽습니다!', CURRENT_TIMESTAMP - INTERVAL 12 DAY, 5),
(13, 11, 5, 'M2 칩셋 정말 빠릅니다. 작업용으로 최고예요.', CURRENT_TIMESTAMP - INTERVAL 11 DAY, 6),
(14, 12, 5, '노이즈 캔슬링이 엄청 강력합니다. 음질도 너무 좋아요.', CURRENT_TIMESTAMP - INTERVAL 10 DAY, 7),
(15, 13, 4, '장시간 사용하면 귀가 좀 아프긴 해요.', CURRENT_TIMESTAMP - INTERVAL 9 DAY, 7),
(16, 15, 5, '손목에 딱 맞고 기능이 정말 많아요. 운동할 때 최고!', CURRENT_TIMESTAMP - INTERVAL 8 DAY, 9),
(17, 16, 5, '디자인이 집 인테리어랑 너무 잘 어울립니다.', CURRENT_TIMESTAMP - INTERVAL 7 DAY, 10),
(18, 17, 4, '수납공간이 넓고 활용도가 좋아요.', CURRENT_TIMESTAMP - INTERVAL 6 DAY, 10);

-- 트랜잭션 반영
COMMIT;
-- 트랜잭션 취소
ROLLBACK;