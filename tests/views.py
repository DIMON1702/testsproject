from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, TemplateView, FormView

from .models import Test, Question, Answer
from .forms import QuestionForm

def home(request):
    tests = Test.objects.all()
    return render(request, 'home.html', {'tests': tests})

def test_view(request, id):
    test = get_object_or_404(Test, id=id)
    questions = Question.objects.filter(test_id=id)
    if request.method == 'POST':
        return render(request, 'test_list.html', {'test': test})
    return render(request, 'test_view.html', {'test': test})

@login_required
def test_create(request):
    return render(request, 'test_create.html')

class TestListView(ListView):
    model = Test

    def get_queryset(self):     
        queryset = super(TestListView, self).get_queryset()
        return  queryset.filter()


def test_list(request, id):
    test = get_object_or_404(Test, id=id)
    questions = Question.objects.filter(test_id=id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        #if form.is_valid():
        #    return render(request, 'test_list.html', {'form': form, 'test': test, 'questions': questions}) 
        #else:
        #    return redirect('home')#form = QuestionForm(request.POST)
    return render(request, 'test_list.html', {'test': test, 'questions': questions})


def question_form(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        form.save()
        return redirect('home')
        if form.is_valid():
            return redirect('home')
    else:
        form = QuestionForm()
    return render(request, 'test_list.html', {'form': form})


'''class QuizTake(FormView):
    form_class = QuestionForm

    def get_form(self, *args, **kwargs):
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(QuizTake, self).get_form_kwargs()

        return dict(kwargs, question=self.question)'''

