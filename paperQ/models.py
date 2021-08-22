from datetime import timedelta
from django.db import models
from django.utils import timezone

# Create your models here.
class QuestionGroup(models.Model):
    name = models.CharField(max_length=200)
    answer_time = models.DurationField(default=timedelta())

    def __str__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=50)
    question_group = models.ForeignKey(QuestionGroup,null=True, on_delete=models.SET_NULL, related_name='person')
    start_time = models.DateTimeField(default=timezone.now)
    rest_time = models.DurationField(default=timedelta())
    score = models.IntegerField(default=-1)

    def __str__(self):
        return self.name

class Question(models.Model):
    index = models.IntegerField(default=0)
    group = models.ForeignKey(QuestionGroup, null=True, on_delete=models.CASCADE, related_name='question')
    q_text = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.group}: No.{self.index}'
 
    class Meta:
        ordering = ['index']

class Answer(models.Model):
    person = models.ForeignKey(Person, null=True, on_delete=models.CASCADE, related_name='answer')
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE, related_name='answer')
    ans_text = models.CharField(max_length=100)

    class Meta:
        ordering = ['question'] 
