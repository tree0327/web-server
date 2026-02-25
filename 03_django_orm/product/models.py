from django.db import models

# 상품 테이블
class Product(models.Model):
    name = models.CharField(max_length=100)  # 최대 100자 문자열 필드
    description = models.TextField(blank=True)  # 폼 입력시 비워둘 수 있는 텍스트 필드
    price = models.PositiveIntegerField()    # 양수 숫자형 필드
    stock = models.PositiveIntegerField()    # 양수 숫자형 필드
    available = models.BooleanField(default=True)  # 기본값이 True인 불리언 필드
    created_at = models.DateTimeField(auto_now_add=True)  # 최초 생성 시간을 자동 저장하는 필드
    updated_at = models.DateTimeField(auto_now=True)  # 수정시 현재 시간을 자동 저장하는 필드
    
    # 객체를 문자열로 표현할 때 사용
    def __str__(self):
        return self.name  # 객체 출력시 상품명 반환

# 할인 정보 테이블 (Product와 Discount 1:1로 연결)
class Discount(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='discount')  # 상품 1개 : 할인정보 1개 연결
    # 할인율 (소수점 5자리, 소수점 이하 2자리)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text='Discount Percentage: (e.g 0.10 for 10%)')
    start_date = models.DateTimeField()  # 할인 시작 시간
    end_date = models.DateTimeField()    # 할인 종료 시간

    def __str__(self):
        return f'{self.discount_percentage}% off for {self.product.name}'  # 객체 출력시 할인율과 상품명 반환

# 리뷰 테이블 (Product와 Review를 1:N으로 연결)
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')  # 여러 리뷰가 하나의 상품을 참조
    user_id = models.PositiveIntegerField(blank=True, null=True)  # 사용자 id (폼에 공란, DB null 허용)
    rating = models.PositiveIntegerField(default=1, help_text='Rating from 1 to 5')  # 기본값 1 별점
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 리뷰작성 시간

    def __str__(self):
        return f'Review for {self.product.name} by {self.user_id}'  # 상품명과 사용자 id 반환

# 카테고리 테이블 (Product와 Category를 N:M 으로 연결)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # 중복이 없는 100자 문자열 필드
    product = models.ManyToManyField(Product, related_name='categories')  # 여러 상품과 여러 카테고리를 연결

    def __str__(self):
        return self.name