from product.models import Product, Review, Discount, Category
from datetime import datetime, timedelta
from django.db.models import Count, Avg, Max
from django.utils import timezone

# 1. 특정 제품의 이름에 "Phone"이 포함된 제품들을 조회
Product.objects.filter(name__icontains='Phone')

# 2. 특정 카테고리 이름이 "가전"인 카테고리에 속한 모든 제품을 조회
Product.objects.filter(categories__name='가전')

# 3. 리뷰가 없는 제품들을 조회
Product.objects.filter(reviews__isnull=True)

# 4. 평점이 4 이상인 리뷰가 달린 제품을 조회
Product.objects.filter(reviews__rating__gte=4).distinct()

# 5. 특정 할인율(예: 10%)보다 높은 할인을 적용받는 제품을 조회
Product.objects.filter(discount__discount_percentage__gt=0.10)

# 6. 특정 날짜 (2025/02/01) 이후에 시작된 할인 정보를 가진 제품들을 조회
Product.objects.filter(discount__start_date__gt='2025-02-01')

# 7. "패션"이라는 이름이 포함된 카테고리에 속한 모든 제품을 조회
Product.objects.filter(categories__name__icontains='패션').distinct()

# 8. 3개 이상의 카테고리에 속한 제품을 조회
Product.objects.annotate(category_count=Count('categories')).filter(category_count__gte=3)

# 9. 재고가 10이하인 제품들을 조회
Product.objects.filter(stock__lte=10)

# 10. "최상"라는 단어가 설명(description)에 포함된 제품들을 조회
Product.objects.filter(description__icontains='최상')

# 11. 이번달에 작성된 리뷰 조회
now = timezone.now()
Review.objects.filter(created_at__year=now.year, created_at__month=now.month)

# 12. 현재 할인중인 제품을 조회
now = timezone.now()
Product.objects.filter(
    discount__start_date__lte=now,
    discount__end_date__gte=now
)

# 13. 리뷰 수가 3개 이상인 제품들을 조회
Product.objects.annotate(review_count=Count('reviews')).filter(review_count__gte=3)

# 14. 특정 사용자(user_id = 2)가 작성한 모든 리뷰를 조회
Review.objects.filter(user_id=2)

# 15. 평균 평점이 4.5 이상인 제품들을 조회
Product.objects.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=4.5)

# 16. 특정 카테고리(가전)의 제품들 중 가격이 100,000원 이상인 제품을 조회
Product.objects.filter(categories__name='가전', price__gte=100000).distinct()

# 17. 20% 이상의 할인율을 적용받는 모든 제품을 조회
Product.objects.filter(discount__discount_percentage__gte=0.20)

# 18. 가격이 50,000원 이상이고 재고가 10개 이상인 제품을 조회
Product.objects.filter(price__gte=50000, stock__gte=10)

# 19. 5점 만점 리뷰가 하나라도 달린 제품을 조회
Product.objects.filter(reviews__rating=5).distinct()

# 20. 가장 최근 리뷰가 작성된 제품을 조회
Product.objects.annotate(latest_review=Max('reviews__created_at')).order_by('-latest_review').first()