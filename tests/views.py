from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import json
from django.http import JsonResponse
from .models import Test, Question, Answer, Comment, TestResult
from .forms import AddTest


def home(request):
    return render(request, 'home.html')


def all_tests(request):
    view = "all"
    if 'q' in request.GET and request.GET['q']:
        if request.GET['q'].strip():
            query_string = request.GET.get('q')
            seens = Test.objects.filter(name=query_string)
        else:
            seens = None
        return render(request, 'all_tests.html', {'seens': seens})
    else:
        if 'order_by' in request.GET:
            tests = Test.objects.all().order_by('created_date')
        else:
            tests = Test.objects.all().order_by('-created_date')
        user = request.user
        tests_results = TestResult.objects.filter(user_id=user.id)

        if 'view' in request.GET:
            view = "only_passed"

    return render(request, 'all_tests.html', {'tests': tests, 'tests_results': tests_results, 'user': user, 'view': view})


def test_view(request, id):
    test = get_object_or_404(Test, id=id)
    if request.method == 'POST':
        try:
            test_res = TestResult.objects.get(
                test_id=id, user_id=request.user.id)
        except ObjectDoesNotExist:
            return redirect('test_list', test.id)
        else:
            return render(request, 'test_result.html', {'result': test_res.correct_answers, 'percent_res': test_res.correct_answers_percent})

    return render(request, 'test_view.html', {'test': test})


@login_required
def test_create(request):
    if request.method == 'POST':
        form = AddTest(request.POST)
    else:
        form = AddTest()
    return render(request, 'test_create.html', {'form': form})


@login_required
def test_list(request, id):
    test = get_object_or_404(Test, id=id)
    questions = Question.objects.filter(test_id=id)
    return render(request, 'test_list.html', {'test': test, 'questions': questions})


def test_result(request):
    if request.method == 'POST':
        correct_answers = 0
        test_question_id = -1
        user_answers = request.POST
        question_count = len(user_answers)-1
        for question in user_answers:
            if question != 'csrfmiddlewaretoken':
                test_question_id = question
                if Answer.objects.get(id=user_answers[question]).is_right is True:
                    correct_answers += 1
        try:
            correct_answers_percent = correct_answers/question_count*100
        except ZeroDivisionError:
            correct_answers_percent = 0

        if test_question_id != -1:
            test_id = Question.objects.get(id=test_question_id).test_id
            test = Test.objects.get(id=test_id)
            test.pass_counter += 1
            test.save()

            test_result = TestResult(
                test_id=test_id, correct_answers=correct_answers, correct_answers_percent=correct_answers_percent, user_id=request.user.id)
            test_result.save()

            return render(request, 'test_result.html', {'result': correct_answers, 'percent_res': correct_answers_percent})
    else:
        return redirect('all_tests')

    return render(request, 'test_result.html')


@login_required
def new_comment(request, id):
    test = get_object_or_404(Test, id=id)
    if request.method == 'POST':
        message = request.POST['message']
        comment = Comment.objects.create(
            text=message,
            test_id=id,
            created_by=request.user
        )

        return redirect('test_view', test.id)
    return render(request, 'new_comment.html', {'test': test})


def test_json(request):
    if request.method == 'POST':
        new_test = json.loads(request.POST['jsonObj'])
        test_name = new_test["test_name"]
        test_description = new_test["test_description"]
        questions = new_test["questions"]
        user = request.user
        test = Test.objects.create(
            name=test_name,
            description=test_description,
            created_by=user
        )
        for question in questions:
            question_name = question["text"]
            new_question = Question.objects.create(
                name=question_name,
                test=test
            )
            answers = question["answers"]
            for answer in answers:
                new_answer = Answer.objects.create(
                    text=answer["answer_text"],
                    is_right=answer["isCorrect"],
                    question=new_question
                )
        return JsonResponse({'redirect_url': 'all_tests'})
