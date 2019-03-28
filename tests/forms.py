from django import forms
from .models import Test, Question, Answer


class AddTest(forms.ModelForm):
    class Meta:
        model = Test
        question_model = Question
        answer_model = Answer
        fields = ('name', 'description', 'created_by')


class AddQuestion(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('name', 'test')


class AddAnswer(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text', 'question', 'is_right')
