from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, TemplateView, FormView

from .models import Test, Question, Answer, Comment, TestResult
from .forms import QuestionForm

def home(request):
    tests = Test.objects.all()
    return render(request, 'home.html', {'tests': tests})

def test_view(request, id):
    test = get_object_or_404(Test, id=id)
    questions = Question.objects.filter(test_id=id)
    comments = Comment.objects.filter(test_id=id)
    if request.method == 'POST':
        return redirect('test_list', test.id)#render(request, 'test_list.html', {'test': test})
    return render(request, 'test_view.html', {'test': test})

@login_required
def test_create(request):
    return render(request, 'test_create.html')

'''class TestListView(ListView):
    model = Test

    def get_queryset(self):     
        queryset = super(TestListView, self).get_queryset()
        return  queryset.filter()
'''

def test_list(request, id):
    test = get_object_or_404(Test, id=id)
    questions = Question.objects.filter(test_id=id)
    
    #if request.method == 'POST':
    #    form = QuestionForm(request.POST)
    #    return redirect('test_result')
        #if form.is_valid():
        #    return render(request, 'test_list.html', {'form': form, 'test': test, 'questions': questions}) 
        #else:
        #    return redirect('home')#form = QuestionForm(request.POST)
    return render(request, 'test_list.html', {'test': test, 'questions': questions})

'''class QuizTake(FormView):
    form_class = QuestionForm

    def get_form(self, *args, **kwargs):
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(QuizTake, self).get_form_kwargs()

        return dict(kwargs, question=self.question)'''

def test_result(request):
    if request.method == 'POST':
        correct_answers = 0
        test_question_id = -1
        user_answers = request.POST
        question_count= len(user_answers)-1
        for question in user_answers:
            if question != 'csrfmiddlewaretoken' :
                test_question_id = question
                if Answer.objects.get(id=user_answers[question]).is_right is True:
                    correct_answers += 1
        try:
            correct_answers_percent = correct_answers/question_count*100
        except ZeroDivisionError:
            correct_answers_percent = 0
        
        test_id = Question.objects.get(id=test_question_id).test_id
        test = Test.objects.get(id=test_id)
        test.pass_counter += 1
        test.save()

        try:
            TestResult.objects.get(test_id=test_id, user_id=request.user.id)
        except :
            test_result = TestResult(test_id=test_id, correct_answers=correct_answers, user_id=request.user.id)
            test_result.save()


        return render(request, 'test_result.html', {'result': correct_answers, 'percent_res': correct_answers_percent})
        

    return render(request, 'test_result.html')