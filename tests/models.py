from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Test(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    pass_counter = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    #created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tests')
    #question = models.ForeignKey(Question, related_name='tests')
    #comment = models.ForeignKey(Comment, related_name='tests')

    def __str__(self):
        return self.name

    def get_questions(self):
        return Question.objects.filter(test=self)

    def get_comments(self):
        return Comment.objects.filter(test=self)


class Question(models.Model):
    name = models.CharField(max_length=100)
    test = models.ForeignKey(Test, related_name='questions')

    # class Meta:
    #    verbose_name = "Question"

    def __str__(self):
        return self.name

    def get_answers(self):
        return Answer.objects.filter(question=self)


class Answer(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, related_name='answers')
    is_right = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.CharField(max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='comments')
    test = models.ForeignKey(Test, related_name='comments')

    def __str__(self):
        return self.text


class TestResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='testresults')
    test = models.ForeignKey(Test, related_name='testresults')
    correct_answers = models.IntegerField()
    correct_answers_percent = models.FloatField()
