from django.shortcuts import render  # 템플릿 렌더링
from django.http import HttpResponse  # 문자열 응답 반환 클래스

# /first/ 요청이 들어왔을 때 Hello django!!! 응답 반환
def index(request):
    # print(type(request))  
    # print(request)
    return HttpResponse('Hello django!!!')

# /first/helloworld 요청이 들어왔을 때 Hello World!!! 응답 반환
def helloworld(request):
    return HttpResponse('Hello World!!!')