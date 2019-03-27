from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, TemplateView, FormView
from django.core.exceptions import ObjectDoesNotExist

from .models import Test, Question, Answer, Comment, TestResult
#from .forms import QuestionForm


def home(request):
    return render(request, 'home.html')

# TODO:  search, filter forpassed tests


def all_tests(request):
    tests = Test.objects.all().order_by('-created_date')
    tests_results = TestResult.objects.all()
    user = request.user
    return render(request, 'all_tests.html', {'tests': tests, 'tests_results': tests_results, 'user': user})


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
        # render(request, 'test_list.html', {'test': test})

    return render(request, 'test_view.html', {'test': test})

# TODO: 4th step
@login_required
def test_create(request):
    # if request.method == 'POST':

    return render(request, 'test_create.html')


'''class TestListView(ListView):
    model = Test

    def get_queryset(self):
        queryset = super(TestListView, self).get_queryset()
        return  queryset.filter()
'''


@login_required
def test_list(request, id):
    test = get_object_or_404(Test, id=id)
    questions = Question.objects.filter(test_id=id)
    return render(request, 'test_list.html', {'test': test, 'questions': questions})


# @login_required
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
        # else: #TODO: request to test_list
        #    return render(request, 'test_view.html', {'test': test})

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
