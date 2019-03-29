from django import forms
from .models import Test, Question, Answer


class AddTest(forms.ModelForm):
    class Meta:
        model = Test
        question_model = Question
        answer_model = Answer
        fields = ('name', 'description', 'created_by')
