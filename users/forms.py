from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from users.models import Student, Teacher, User


class StudentAddForm(UserCreationForm):
    std = forms.CharField() 
    
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'email' , 'username' , 'is_male' ,'profile_image']
  
    def __init__(self, *args, **kwargs) -> None:
        condition = kwargs.pop('condition',None)
        super(StudentAddForm,self).__init__(*args, **kwargs)

        if condition:
            del self.fields['std']
            self.fields['subject'] = forms.CharField()
            self.fields['contact no'] = forms.CharField()            

        for name,field in self.fields.items():
             
            field.widget.attrs.update(
                {'class' : 'form-control','placeholder': f'Enter {field.label}' }
            )

            if name == 'is_male':
                field.label ='Male'
                field.widget.attrs.update(
                {'class' : 'form-check-label' }
                )
        

class ContactForm(ModelForm):
    
    class Meta:
        model = Student
        fields = ['guardian' ,'contact_no' , 'address']
    
    def __init__(self, *args, **kwargs) -> None:
        super(ContactForm,self).__init__(*args, **kwargs)

        for name,field in self.fields.items():

            if name == 'address':
                field.widget = forms.Textarea(attrs = {'rows' :6, 'cols' :10})

            field.widget.attrs.update(
                {'class' : 'form-control','placeholder': f'Enter {field.label}' }
            )

class TeacherForm(ModelForm):
    
    class Meta:
        model = Teacher
        exclude =['user']
    
    def __init__(self, *args, **kwargs) -> None:
        super(TeacherForm,self).__init__(*args, **kwargs)

        for name,field in self.fields.items():

            if name == 'address':
                field.widget = forms.Textarea(attrs = {'rows' :6, 'cols' :10})

            field.widget.attrs.update(
                {'class' : 'form-control','placeholder': f'Enter {field.label}' }
            )

    def clean(self):
        data = self.cleaned_data
        a = Teacher.vacant_posts()
        if not a:
            raise forms.ValidationError('No vacant posts')
        elif data['sub'].name in a:
            raise forms.ValidationError('No vacant post for the specifed subject')
        return super().clean()
class UpdateStudentForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'email' , 'username' , 'is_male' ,'profile_image']

    
    def __init__(self, *args, **kwargs) -> None:
        super(UpdateStudentForm,self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
             
            field.widget.attrs.update(
                {'class' : 'form-control','placeholder': f'Enter {field.label}' }
            )

            if name == 'is_male':
                field.label ='Male'
                field.widget.attrs.update(
                {'class' : 'form-check-label' }
                )
    