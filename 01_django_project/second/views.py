from django.shortcuts import render  # 템플릿 렌더링


# /second/ 요청이 들어왔을 때 템플릿 HTML을 반환
def index(request):
    return render(request, 'second/index.html')  # template 폴더 기준 (상대)경로로 HTML 파일 렌더링