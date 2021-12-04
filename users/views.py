from django.contrib  import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import TemplateView,CreateView,ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView

from subjects.models import Subject
from .forms import ContactForm, StudentAddForm, TeacherForm, UpdateStudentForm
from .models import Student, Teacher, User
from .mixins import TeacherMixin,StudentMixin,OwnerMixin

# Create your views here.


class HomePage(TemplateView):
    template_name = 'home.html'


class StudentAdd(CreateView):
    form_class = StudentAddForm
    template_name = 'users/student_add.html'
    
    def form_valid(self, form = StudentAddForm):
        x = self.get_form_kwargs().get('data').get('std')
        temp = form.save()
        try:
            rollno = int(Student.fil.get_max_rollno(x)[0]['rollno'].split('X')[1])
            if not rollno:
                rollno = 0                
        except:
            rollno = 0
        rollno = x + str(rollno + 1)

        #create student
        Student.objects.create(
            user = temp,
            rollno= rollno,
            std = x
        )
        print(temp)
        auth_login(self.request , temp)
        print(self.request.user, self.request.user.is_authenticated)
        self.object = temp
        messages.success(self.request, f'Student{self.object} Created')
        return redirect('contact-add', self.object.student.id)


class Contactadd(LoginRequiredMixin,UpdateView):
    form_class = ContactForm
    template_name = 'users/student_add.html'
    queryset = Student.objects.all()

    def get_success_url(self) :
        messages.success(self.request, f'Student{self.object} Contact details saved')
        return reverse('home')

    def get_context_data(self, **kwargs):
        kwargs['page'] = 'contact' 
        return super().get_context_data(**kwargs)


class StudentsList(LoginRequiredMixin,ListView):
    
    template_name = 'users/students.html'
    context_object_name = 'students'

    def get_queryset(self) :
        if self.request.user.is_student:
            std = Student.objects.get(user= self.request.user).std
            return Student.objects.filter(std = std)
        return Student.objects.all()


class StudentDelete(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    queryset = User.objects.filter(is_student = True)
    template_name = 'users/user_confirm_delete.html'
    success_url = '/' 
    
    def test_func(self):
        obj = self.get_object()
        return True if not self.request.user.is_student or self.request.user == obj else False        


class UpdateStudent(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    template_name = 'users/student_update.html'
    queryset = User.objects.all()

    def test_func(self):
        obj = self.get_object()
        return True if not self.request.user.is_student or self.request.user == obj else False
    
    def dispatch(self, request, *args, **kwargs) :
        pk = self.kwargs['pk']    
        self.initial1 = self.get_queryset().get(id = pk)
        self.prefix1 = 'student_form'
        self.initial2 = self.get_queryset().get(id = pk).student
        self.prefix2 = 'contact_form'
        return super().dispatch(request, *args, **kwargs)
        
    def get_form(self, form_class= None):        
        return (UpdateStudentForm(instance = self.initial1,prefix =self.prefix1) , ContactForm(instance = self.initial2 ,prefix =self.prefix2))

    def get_context_data(self, **kwargs):
        student_form , contact_form = self.get_form()
        kwargs['student_form'] = student_form
        kwargs['contact_form'] = contact_form
        return kwargs

    def get_success_url(self) :
        messages.success(self.request, f'Student{self.object} details updated')
        return reverse('home')
    
    def form_invalid(self, contact_form, student_form, **kwargs):
        contact_form.prefix='contact_form'
        student_form.prefix='student_form'
        return self.render_to_response(
            self.get_context_data(kwargs= {'contact_form':contact_form, 'student_form':student_form}))
    
    def post(self, request, *args, **kwargs):
        student_form  = UpdateStudentForm(
            self.request.POST,
            self.request.FILES,
            instance = self.initial1,
            prefix = self.prefix1)
        contact_form = ContactForm(
            self.request.POST,
            instance = self.initial2,
            prefix = self.prefix2)
        if student_form.is_valid() and contact_form.is_valid():
            self.object=student_form.save()
            contact_form.save() 
            return HttpResponseRedirect(self.get_success_url()) 
        else:
            return self.form_invalid(contact_form, student_form ,**kwargs)


class TeacherAdd(CreateView):
    form_class = StudentAddForm
    template_name = 'users/student_add.html'
    success_url = '/'

    def get_form_kwargs(self) :
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
            'condition': True,
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs
    
    def get_context_data(self, **kwargs) :
        posts = Teacher.vacant_posts()
        kwargs.update({'posts' :posts})
        return super().get_context_data(**kwargs)

    def form_valid(self, form=StudentAddForm):
        sub ,contact = form.cleaned_data['subject'] ,form.cleaned_data['contact no']
        temp = form.save(commit =False)
        temp.is_student= False
        form.save()
        
        try:
            subject = Subject.objects.filter(name__startswith = sub[:3].upper()).first()
        except:
            subject = Subject.objects.filter(name__contains = sub[:4].upper()).first()
        if not subject:
            subject =Subject.objects.get(name = 'PHYSICS')
        Teacher.objects.create(
            user = temp,
            sub = subject,
            contact_no = contact
        )
        messages.success(self.request , f'{temp} Created')
        return super().form_valid(form)



class TeachersList(LoginRequiredMixin,ListView):
    queryset = Teacher.objects.all()
    template_name = 'users/students.html'
    context_object_name = 'students'

    def get_context_data(self, **kwargs):
        kwargs['page'] = 'teacher'
        return super().get_context_data(**kwargs)


class TeacherUpdate(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    
    queryset = User.objects.filter(is_student =False)
    fields = '__all__'
    template_name = 'users/teacherform.html'

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']    
        self.initial1 = self.get_queryset().get(id = pk)
        self.prefix1 = 'teacher_form'
        self.initial2 = self.get_queryset().get(id = pk).teacher
        self.prefix2 = 'contact_form'
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class= None):        
        return (UpdateStudentForm(instance = self.initial1,prefix =self.prefix1) , TeacherForm(instance = self.initial2 ,prefix =self.prefix2))

    def get_context_data(self, **kwargs):
        teacher_form , contact_form = self.get_form()
        kwargs['teacher_form'] = teacher_form
        kwargs['contact_form'] = contact_form
        return kwargs
    
    def post(self, request, *args, **kwargs):
        teacher_form  = UpdateStudentForm(
            self.request.POST,
            self.request.FILES,
            instance = self.initial1,
            prefix = self.prefix1)
        contact_form = ContactForm(
            self.request.POST,
            instance = self.initial2,
            prefix = self.prefix2)
        if teacher_form.is_valid() and contact_form.is_valid():
            self.object=teacher_form.save()
            contact_form.save() 
            return HttpResponseRedirect(reverse('profile', kwargs= {'pk': self.object.id}) ) 
        else:
            return self.form_invalid(contact_form, teacher_form ,**kwargs)


class TeacherDelete(LoginRequiredMixin,OwnerMixin,DeleteView):
    # queryset = User.objects.all()
    model = User
    # success_url = reverse_lazy('home')

    def get_success_url(self):
        messages.info(self.request,'Deleted')
        return reverse('home')


class Profile(LoginRequiredMixin,UserPassesTestMixin,DetailView):
    template_name = 'users/profile.html'
    model = User

    def test_func(self):
        return self.request.user == User.objects.get(id = self.kwargs['pk'])
