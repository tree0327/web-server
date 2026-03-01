from product.models import Product, Category, Discount, Review  # 모델 객체
from django.db.models import Sum, Avg, Count, Max, Min          # 집계함수
from datetime import datetime, timedelta                        # 날짜 계산
from django.utils import timezone

# 1:N Product-Review
# 1. 특정 제품(Product)의 모든 리뷰 가져오기
reviews = Review.objects.filter(product_id=1)  # 필터링을 통해 조회하는 방식
reviews
for review in reviews:
    print(review.id, review.product, review.user_id, review.rating, review.comment)

# 상품 객체를 이용해 조회하는 방식
product = Product.objects.get(id=1)
Review.objects.filter(product=product)

# related_name을 이용해 검색하는 방식
product.reviews
product.reviews.all()

# 2. 특정 제품(Product)의 평균 평점과 리뷰 개수 확인
product = Product.objects.get(id=1)
product.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']  # 1번 상품의 리뷰의 평균 평점
product.reviews.count()  # 리뷰 개수

# 3. 평점이 높은 리뷰(예: 4점 이상)만 가져오기
high_rating_reviews = product.reviews.filter(rating__gte=4)  # 평점이 4점 이상인 리뷰
for review in high_rating_reviews:
    print(f'[High Rating] User ID: {review.user_id}, Rating: {review.rating}, Comment: {review.comment}')

# 4. 모든 제품의 평균 평점과 리뷰 개수 가져오기
products_with_review_data = Product.objects.annotate(
    avg_rating = Avg('reviews__rating'),  # 각 상품의 평균 평점
    review_count = Count('reviews')       # 각 상품의 리뷰 개수
)
for product in products_with_review_data:
    avg_rating = f"{product.avg_rating:.2f}" if product.avg_rating else "0"  # 평균 평점 포맷 처리
    print(f"Product: {product.name}, Average Rating: {avg_rating}, Reviews: {product.review_count}")  # 상품별 리뷰 통계

# 1:1 Product-Discount
# 1. 특정 제품(Product)의 할인 정보 가져오기
product_id = 3
try:
    discount = Discount.objects.get(product_id=product_id)  # 3번 제품의 할인정보
    print(f"Product: {discount.product.name}, Discount: {discount.discount_percentage*100}%, Start: {discount.start_date}, End: {discount.end_date}")
except Discount.DoesNotExist:  # 할인 정보가 없어 오류시
    print(f'Product with ID {product_id} has no discount information.')

# 2. 할인 중인 모든 제품 가져오기
current_date = timezone.now()
current_discounts = Discount.objects.filter(start_date__lte=current_date, end_date__gte=current_date)  # 시작시간~종료시간 사이의 할인정보

for discount in current_discounts:
    print(f'Product: {discount.product.name}, Discount: {discount.discount_percentage}%, Ends on: {discount.end_date}')

# 3. 특정 할인율 이상인 제품 가져오기 (예: 20% 이상)
high_discounts = Discount.objects.filter(discount_percentage__gte=0.2)  # 할인율이 20% 이상인 할인

for discount in high_discounts:
    print(f'Product: {discount.product.name}, Discount: {discount.discount_percentage}%, Ends on: {discount.end_date}')

# 4. 할인 정보와 함께 모든 제품 가져오기
product = Product.objects.all()  # 전체 상품 조회
products_with_discounts = Product.objects.prefetch_related('discount')  # 할인 정보 미리 조회 설정

for product in products_with_discounts:
    if hasattr(product, 'discount'):  # 할인 정보(속성)이 있으면
        print(f"Product: {product.name}, Discount: {product.discount.discount_percentage*100}%, Ends: {product.discount.end_date}")
    else:  # 할인 정보가 없으면
        print(f"Product: {product.name}, No discount available")

# 5. 할인 기간이 지난 제품 가져오기
expired_discounts = Discount.objects.filter(end_date__lt=current_date)  # 종료일이 현재보다 이전의 할인정보

for discount in expired_discounts:
    print(f"[Expired Discount] Product: {discount.product.name}, Discount: {discount.discount_percentage*100}% (Ended on: {discount.end_date})")

# 카테고리 테이블 (N:M Product-Category)
# 1. 특정 제품(Product)이 속한 모든 카테고리 가져오기
product_id = 9
product = Product.objects.get(id=product_id)
categories = product.categories.all()  # 해당 상품에 연결된 모든 카테고리 조회

print(f'제품: {product.name}에 해당하는 카테고리는?')
for category in categories:
    print(f"- {category.name}")

# 2. 특정 카테고리(Category)에 속한 모든 제품 가져오기
category_name = '가전'
try:
    category = Category.objects.get(name=category_name)
    products = category.product.all()

    print(f'카테고리: {category.name}에 해당하는 제품은?')
    for product in products:
        print(f"- {product.name} (Price: {product.price}, Stock: {product.stock})")
except Category.DoesNotExist:
    print(f"카테고리 '{category.name}'은 존재하지 않아요. ")

# 3. 카테고리가 없는 제품(Product) 가져오기
products_without_category = Product.objects.filter(categories__isnull=True)  # 연결된 카테고리가 없는 상품
print("카테고리 없는 상품은?")
for product in products_without_category:
    print(f"- {product.name} (Price: {product.price}, Stock: {product.stock})")

# 4. 특정 제품(Product)에 새 카테고리 추가하기
new_category_name = "Seasonal"
new_category, created = Category.objects.get_or_create(name=new_category_name)  # 카테고리가 없으면 생성, 있으면 기존 객체 반환
product.categories.add(new_category)  # 카테고리가 없는 제품에 새 카테고리를 연결

print(f"추가된 카테고리 '{new_category.name}' 적용 제품은 '{product.name}'.")

# 5. 모든 카테고리와 각 카테고리의 제품 수 출력하기
categories_with_product_count = Category.objects.annotate(product_count=Count('product'))  # 카테고리별 상품 수 집계하고 추가

for category in categories_with_product_count:
    print(f"카테고리: {category.name}, 제품 수: {category.product_count}")

# 6. 여러 카테고리에 속한 제품(Product) 가져오기
multi_category_products = Product.objects.annotate(category_count=Count('categories')).filter(category_count__gt=1)  # 카테고리가 2개 이상인 상품

print("다중 카테고리 제품은?")
for product in multi_category_products:
    print(f"- {product.name} (Categories: {product.categories.count()})")

### N + 1 이슈 대응 ###
# 1. select_related    : ForeignKey, OneToOne처럼 단일 객체 관계를 JOIN으로 함께 조회할 때 사용
# 2. prefetch_related  : ManyToMany, 역참조처럼 여러 객체 관계를 별도 쿼리로 미리 조회할 때 사용

# 할인하는 상품 목록 조회 1
products = Product.objects.all()
for product in products:
    if hasattr(product, 'discount'):  # 할인 정보(속성)이 있으면
        print(f"Product: {product.name}, Discount: {product.discount.discount_percentage*100}%, Ends: {product.discount.end_date}")
    else:  # 할인 정보가 없으면
        print(f"Product: {product.name}, No discount available")

# 할인하는 상품 목록 조회 2 : Select_related
products_with_discounts = Product.objects.select_related('discount')  # discount를 JOIN으로 함께 조회
for product in products_with_discounts:
    if hasattr(product, 'discount'):  # 할인 정보(속성)이 있으면
        print(f"Product: {product.name}, Discount: {product.discount.discount_percentage*100}%, Ends: {product.discount.end_date}")
    else:  # 할인 정보가 없으면
        print(f"Product: {product.name}, No discount available")

# 상품 목록 조회 1
products = Product.objects.all()
for product in products:
    print(product.name, product.reviews.all())

# 상품 목록 조회 2
products = Product.objects.prefetch_related('reviews')  # reviews를 별도 쿼리로 미리 조회
for product in products:
    print(product.name, product.reviews.all())

# 집계 처리
# 1. aggregate : 전체 조회 결과를 하나로 집계하여 딕셔너리 형태로 반환
Product.objects.aggregate(total_count=Count('id'))   # 전체 상품 수
Product.objects.aggregate(total_price=Sum('price'))  # 전체 상품 가격 합계
Product.objects.aggregate(avg_price=Avg('price'))    # 전체 상품 평균 가격
Product.objects.aggregate(max_price=Max('price'))    # 전체 상품 중 최고 가격
Product.objects.aggregate(min_price=Min('price'))    # 전체 상품 중 최저 가격

# 2. filter + aggregate : 조건에 맞는 데이터만 먼저 걸러서 집계
Product.objects.filter(categories__name='가전')  # 가전제품 조회
Product.objects.filter(categories__name='가전').aggregate(avg_price=Avg('price'))  # 가전 제품들의 평균 가격

# 3. 연관관계 annotate : 각 객체별 집계 결과를 계산해서 객체마다 필드처럼 추가
# .value(...) : 어떤 컬럼 기준으로 결과를 나눌지 결정, .annotate(...) : 그 기준별 집계 수행
# group by : 아래 구문은 Select product.name, count(*) from review group by product_id와 같다.
Review.objects.values('product').annotate(review_counts=Count('id'))  # 상품별 리뷰 수 집계

products = Product.objects.annotate(review_counts=Count('reviews'))  # 각 상품 객체에 review_counts 필드 추가
products_with_review_counts = [(product.name, product.review_counts) for product in products]  # 상품명과 리뷰 수를 리스트로 정리
print(products_with_review_counts)

# 카테고리별 상품개수
Category.objects.values('name').annotate(product_count=Count('product'))  # 카테고리별 상품 수 집계 (추가)
Product.objects.values('categories').annotate(product_count=Count('id'))   # 카테고리 기준으로 상품 수 집계(추가)

categories = Category.objects.annotate(product_count=Count('product'), avg_product_price=Avg('product__price'))  # 각 카테고리에 상품 수, 평균 가격 추가
categories_with_info = [(cate.name, cate.product_count, cate.avg_product_price) for cate in categories]
print(categories_with_info)