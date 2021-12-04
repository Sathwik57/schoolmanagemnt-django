from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Assignment, GradedAssignment,Question
from subjects.forms import AssignmentForm,QuestionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from users.mixins import TeacherMixin

# Create your views here.

class AddAssignment(LoginRequiredMixin,TeacherMixin,CreateView):
    form_class = AssignmentForm
    template_name = 'subjects/addassignment.html'
    
    def get_success_url(self):
        return reverse('add-ques' , kwargs = {'pk':self.object.id})

    def form_valid(self, form=AssignmentForm ):
        temp = form.save(commit = False)
        temp.sub = self.request.user
        form.save()
        return super().form_valid(form)


class DeletetAssignments(LoginRequiredMixin,TeacherMixin,DeleteView):
    model = Assignment
    template_name = 'subjects/question_confirm_delete.html'

    def get_success_url(self):
        return reverse('quiz')

class AddQuestions(LoginRequiredMixin,TeacherMixin,UserPassesTestMixin,CreateView):
    template_name = 'subjects/questionadd.html'
    form_class = QuestionForm

    def test_func(self):
        self.ass = Assignment.objects.get(id = self.kwargs['pk'])
        return self.request.user == Assignment.objects.get(id = self.ass.id).sub
         

    def get_success_url(self):
        return reverse('assignment-detail' ,kwargs={'pk':self.ass.id})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': self.ass})
        return kwargs


    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        kwargs['title'] = self.ass
        kwargs['path'] = self.request.path 
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        instances = form.save(commit = False)
        order = 1
        for instance in instances:
            instance.order =1
            instance.test = self.ass
            instance.save()
            order += 1
        return HttpResponseRedirect( self.get_success_url())


class AssignmentDetail(LoginRequiredMixin,TeacherMixin,DetailView):
    model = Assignment


class UpdateAssignment(LoginRequiredMixin,TeacherMixin,UpdateView):
    model = Assignment
    fields = ('title',)

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        kwargs.update({'obj': obj})
        return super().get_context_data(**kwargs)
    
    def get_success_url(self):
        return reverse('assignment-update', kwargs={'pk' : self.object.id})
    


class UpdateQuestion(LoginRequiredMixin,UserPassesTestMixin ,TeacherMixin,UpdateView):
    model =Assignment
    form_class = QuestionForm
    template_name = 'subjects/question_update.html'

    def test_func(self):
        self.test = Assignment.objects.get(id = self.kwargs['pk'])
        return self.request.user == self.test

    def form_valid(self, form):
        instances = form.save(commit = False)
        self.test = Assignment.objects.get(id = self.kwargs['pk'])
        order  = self.test.get_order()['order__max']
        order = order + 1 if order else 1  
        for instance in instances:
            if not instance.order:
                instance.order = order
            # instance.test = self.ass
            instance.save()
            order += 1
        return HttpResponseRedirect( self.get_success_url())

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('assignment-detail' ,kwargs={'pk':self.object.id})


class DelQuestion(LoginRequiredMixin,TeacherMixin,DeleteView):
    model =Question
    
    def get_success_url(self):
        return reverse('assignment-detail' ,kwargs={'pk':self.object.test.id})


class GradedList(LoginRequiredMixin,TeacherMixin,ListView):
    model = GradedAssignment