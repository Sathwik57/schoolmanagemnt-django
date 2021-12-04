import matplotlib.pyplot as plt
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.views.generic.base import  TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from users.models import Student
# from .utils import get_url
from ..models import GradedAssignment, Question

from ..models import Assignment 
from users.mixins import StudentMixin

class QuizList(ListView):
    model = Assignment
    template_name = 'subjects/quiz_list.html'
 
class TakeQuiz(LoginRequiredMixin,StudentMixin,UserPassesTestMixin,SingleObjectMixin,TemplateView):
    template_name = 'subjects/take_quiz.html'

    def test_func(self):
        self.ass = Assignment.objects.get(id = self.kwargs['pk'])
        self.stdu = Student.objects.get(user =self.request.user)
        if GradedAssignment.objects.filter(assignment =self.ass , student = self.stdu ):
            return False
        return True

    def get_object(self, queryset = None):
        return Assignment.objects.get(id = self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        a = dict(request.POST)
        a.pop('csrfmiddlewaretoken')
        score_dict = self.validate(a)
        values = list(score_dict.values())
        values.pop(0)
        labels = ['correct','wrong','not answered']
        plt.pie(values, labels = labels ,autopct = '%1.1f%%', colors =['blue','orange','grey'])
        plt.legend(loc='lower right')

        name = self.stdu.rollno +'-'+ str(self.get_object().id)
        plt.savefig(f'static/images/grades/{name}.png')
        plt.close()
        url = f'/images/grades/{name}.png'
        a = GradedAssignment.objects.create(
            student = self.stdu,
            assignment = self.get_object(),
            grade =  round(score_dict['score'] * 10/ score_dict['total'],2),
            score = score_dict['score'],
            total = score_dict['total'],
            wrong_answer = score_dict['wrong'],
            img_url = url
        )
        self.object = self.get_object()
        return HttpResponseRedirect(reverse('quiz-result' ,kwargs={'pk':a.pk}))

    def get(self, request, *args, **kwargs) :
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def validate(self , data):
        total,score,wa = 0 , 0 , 0
        print(data)
        for x in data:
            if not data[x][0] =='None':
                print(x,data[x])
                if Question.objects.get(ques = x).check_answer(data[x][0]):
                    total += 1
                    score += 1
                else:
                    total += 1
                    wa += 1
            else:
                print(x,data[x])
                total += 1
        score_dict = {
            'total' : total,
            'score' : score,
            'wrong' : wa,
            'na' : total - score - wa
        }
        return score_dict

#result of single test written by student
class Results(LoginRequiredMixin, UserPassesTestMixin,DetailView):
    model = GradedAssignment
    template_name = 'subjects/results.html'

    def test_func(self) :
        self.obj = self.get_object().student.user
        if  not self.request.user.is_student or self.request.user == self.obj :
            return True
        return False

#list of test results of single user
class ResultsList(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = GradedAssignment

    def get_queryset(self):
        return self.obj.gradedassignment_set.all()

    def test_func(self) :
        self.obj = self.stdu= Student.objects.get(id = self.kwargs['pk'])
        if  not self.request.user.is_student or self.request.user == self.obj.user :
            return True
        return False