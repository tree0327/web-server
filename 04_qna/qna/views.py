from django.shortcuts import render, redirect, resolve_url  # 템플릿 응답, 페이지 이동처리, URL 이름을 실제 경로로 변환
from .models import Question, Answer, QuestionForm  # 질문/답변 모델과 질문 폼
from django.http import Http404, HttpResponseForbidden, JsonResponse  # 404, 403 응답처리, JSON 응답 처리
from django.core.paginator import Paginator         # 페이징 처리 도구
from django.contrib.auth.decorators import login_required  # 로그인 필요 데코레이터
from django.contrib import messages  # 사용자 알림 메시지

# 질문 목록을 조회하고, 페이징 처리하고 목록 페이지를 반환하는 뷰 함수
def index(request):
    # questions = Question.objects.order_by('-created_at')
    questions = Question.objects.prefetch_related('answer_set').select_related('author').order_by('-created_at')  # 답변/작성자를 함께 조회
    page = request.GET.get('page', '1')  # 기본 페이지 1
    paginator = Paginator(questions, 10)  # 페이지당 컨텐츠 수
    page_obj = paginator.get_page(page)  # 현재 페이지 객체 생성
    return render(request, 'qna/index.html', {'page_obj': page_obj})  # 목록 페이지 렌더링

# 질문 번호에 해당하는 상세 페이지를 조회하는 함수
def question_detail(request, question_id):
    print(f'{question_id = }')
    try:
        question = Question.objects.get(id=question_id)  # 질문 객체 조회
        print(f'{question = }')
        return render(request, 'qna/question_detail.html', {'question': question})  # 상세 페이지 렌더링
    except Question.DoesNotExist:
        raise Http404('해당 질문은 존재하지 않습니다.')  # 해당하는 질문이 없으면 404처리

# 질문 작성 폼을 보여주고, 새 질문을 저장하는 함수 (로그인 필수)
@login_required(login_url='uauth:login')
def question_create(request):
    if request.method == 'POST':  # 폼 제출 POST 요청인 경우
        form = QuestionForm(request.POST)  # 폼 생성
        if form.is_valid():
            question = form.save(commit=False)  # DB 저장 전 모델 객체 생성
            question.author = request.user      # 현재 로그인 사용자를 작성자로 지정
            question.save()                     # DB 저장

            print(f'{question = }')
            return redirect('qna:question_detail', question_id=question.id)  # 상세페이지로 이동
    else:
        form = QuestionForm()
    
    return render(request, 'qna/question_form.html', {'form': form})  # 질문 작성 폼 렌더링

# 기존 질문을 수정할 수 있도록 처리하는 함수
@login_required(login_url='uauth:login')
def question_modify(request, question_id):

    question = Question.objects.get(id=question_id)  # 수정할 원본 질문 조회

    # 수정 권한 검사 : 작성자 본인 또는 관리자에 한해 수정 가능
    if request.user != question.author and not request.user.is_staff:
        return HttpResponseForbidden('수정 권한이 없습니다.')  # 권한 없을시 403 응답

    if request.method == 'POST':  # 수정 폼 제출할 경우
        form = QuestionForm(request.POST, instance=question)  # 기존 객체에 덮어쓰기용 폼 생성
        if form.is_valid():
            question = form.save()  # 수정 내용 저장
            return redirect('qna:question_detail', question_id=question_id)  # 상세페이지로 이동
    else:
        form = QuestionForm(instance=question)  # 원본 데이터를 이용해 폼 객체 생성

    return render(request, 'qna/question_form.html', {'form': form})  # 질문 수정 폼 렌더링

# messages프레임워크 레벨
# - messages.success()  # 작업이 정상적으로 완료되었음을 사용자에게 알리는 성공 메시지
# - messages.error()  # 오류 발생 또는 권한 문제 등을 사용자에게 알리는 에러 메시지
# - messages.warning()  # 주의가 필요한 상황임을 알리는 경고 메시지
# - messages.info()  # 단순 정보나 안내 사항을 사용자에게 전달하는 메시지

# 질문 작성자 또는 관리자가 질문을 삭제하는 뷰 함수
@login_required(login_url='uauth:login')
def question_delete(request, question_id):
    
    question = Question.objects.get(id=question_id)  # 삭제할 질문 조회

    # 삭제 권한 검사
    if request.user != question.author and not request.user.is_staff:
        # return HttpResponseForbidden('삭제 권한이 없습니다.')
        messages.error(request, '삭제 권한이 없습니다.')  # 권한 없음 메시지
        return redirect('qna/question_detail', question_id=question_id)  # 상세 페이지로 이동
    
    question.delete()  # 질문 삭제
    return redirect('qna/index')  # 목록 페이지로 이동

# 질문 추천을 추가하거나 취소하고, 결과를 JSON으로 반환하는 함수
@login_required(login_url='uauth:login')
def question_vote(request, question_id):
    question = Question.objects.get(id=question_id)  # 추천 대상 질문 조회

    if request.user == question.author:  # 본인이 추천 누르면
        return JsonResponse({
            'result': 'error',
            'message': '본인이 작성한 글은 추천할 수 없습니다.'
        })
    if question.voters.filter(id=request.user.id).exists():  # 이미 추천한 상황이면
        question.voters.remove(request.user)                 # 추천 취소
    else:
        question.voters.add(request.user)  # 추천한 적 없으면 추천 추가

    # 비동기 요청은 redirect 처리 불필요
    return JsonResponse({
        'result': 'success',
        'vote_count': question.voters.count()  # 현재 추천 수
    })

# 특정 질문에 대한 답변을 생성하는 뷰 함수 (로그인 필수)
@login_required(login_url='uauth:login')
def answer_create(request, question_id):
    content = request.POST.get('content')  # 사용자가 입력한 답변 내용
    print(f'{question_id = }')
    print(f'{content = }')

    # 1. question 객체 조회
    question = Question.objects.get(id = question_id)  # 답변이 달린 현재 질문

    # 2. answer 객체 생성
    answer = Answer.objects.create(question=question, content=content, author=request.user)  # 답변 객체 생성
    print(f'{question_id}번 질문에 {answer.id}번 답변이 생성되었습니다.')

    # POST 요청 후에는 리다이렉트를 통해서 URL을 변경해준다. (새로고침 이슈를 막음)
    return redirect(f'{resolve_url("qna:question_detail", question_id=question_id)}#answer_{answer.id}')  # 상세페이지의 답변 위치로 이동

# 답변 내용을 수정하고, 원래 질문의 상세 페이지로 이동하는 뷰 함수
@login_required(login_url='uauth:login')
def answer_modify(request, answer_id):
    question_id = request.GET.get('question_id')  # 원래 질문 번호 전달받기
    answer = Answer.objects.get(id=answer_id)     # 수정할 답변 조회

    # 수정 권한 검사 : 작성자 본인 또는 관리자에 한해 수정 가능
    if request.user != answer.author and not request.user.is_staff:
        messages.error(request, '수정 권한이 없습니다.')  # 권한 없음 메시지
        return redirect('qna:question_detail', question_id=question_id)  # 상세 페이지로 이동

    if request.method == 'POST':  # 수정 폼 제출할 경우
        content = request.POST.get('content')  # 수정된 답변 내용 가져오기
        answer.content = content  # 수정된 답변 내용 변경
        answer.save()  # 저장
        messages.info(request, '답변을 정상적으로 수정했습니다.')
    return redirect(f"{resolve_url('qna:question_detail', question_id=question_id)}#answer_{answer_id}")  # 수정한 답변 위치로 이동

# 답변 작성자 또는 관리자가 답변을 삭제하는 함수
@login_required(login_url='uauth:login')
def answer_delete(request, answer_id):
    question_id = request.GET.get('question_id')  # 원래 질문 번호
    answer = Answer.objects.get(id=answer_id)  # 삭제할 답변

    # 삭제 권한 검사
    if request.user != answer.author and not request.user.is_staff:
        # return HttpResponseForbidden('삭제 권한이 없습니다.')
        messages.error(request, '삭제 권한이 없습니다.')  # 권한 없음 메시지
        return redirect('qna:question_detail', question_id=question_id)  # 상세 페이지로 이동
    
    answer.delete()  # 질문 삭제
    messages.success(request, '답변을 정상적으로 삭제했습니다.')
    return redirect('qna:question_detail', question_id=question_id)  # 상세 페이지로 이동

# 답변 추천을 추가하거나 취소하고, 결과를 JSON으로 반환하는 함수
@login_required(login_url='uauth:login')
def answer_vote(request, answer_id):
    answer = Answer.objects.get(id=answer_id)  # 추천 대상 답변 조회

    if request.user == answer.author:  # 본인이 추천 누르면
        return JsonResponse({
            'result': 'error',
            'message': '본인이 작성한 답변은 추천할 수 없습니다.'
        })
    if answer.voters.filter(id=request.user.id).exists():  # 이미 추천한 상황이면
        answer.voters.remove(request.user)                 # 추천 취소
    else:
        answer.voters.add(request.user)  # 추천한 적 없으면 추천 추가

    # 비동기 요청은 redirect 처리 불필요
    return JsonResponse({
        'result': 'success',
        'vote_count': answer.voters.count()  # 현재 추천 수
    })