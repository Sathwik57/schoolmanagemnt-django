from django.db import models

from users.models import Student, User

# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name


class Assignment(models.Model):
    sub = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title

    def get_order(self):
        return self.test.aggregate(models.Max('order'))

    def get_question_count(self):
        return self.test.all.count()

class GradedAssignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(
        Assignment,on_delete=models.CASCADE ,null=True,blank='True',related_name='assignment')
    grade = models.FloatField()
    score = models.IntegerField()
    wrong_answer = models.IntegerField()
    total = models.IntegerField()
    img_url = models.CharField(max_length = 250, null = True , blank= True )

    class Meta:
        constraints = [
            models.constraints.UniqueConstraint(fields = ['student','assignment'] ,name = 'unique_test')
        ]

    def __str__(self) -> str:
        s = self.assignment.title if self.assignment else 'None'
        return s + '-' + self.student.user.username

    def not_answered(self):
        return self.total - self.score -self.wrong_answer

class Question(models.Model):
    test = models.ForeignKey(Assignment, on_delete=models.CASCADE ,related_name='test')
    ques = models.CharField(max_length = 250)
    option1 = models.CharField(max_length = 100)
    option2 = models.CharField(max_length = 100)
    option3 = models.CharField(max_length = 100)
    option4 = models.CharField(max_length = 100)
    answer = models.IntegerField()
    order = models.SmallIntegerField()

    def __str__(self) -> str:
        return self.ques

    def check_answer(self, option):
        if int(option) == self.answer:
            return True 
        return False