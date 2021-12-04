from django.forms.models import ModelForm
from django.forms import inlineformset_factory
from django.forms.widgets import Textarea

from .models import Assignment,Question


class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = ['title',]

    def __init__(self, *args, **kwargs) -> None:
        super(AssignmentForm,self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
             
            field.widget.attrs.update(
                {'class' : 'form-control','placeholder': f'Enter {field.label}' }
            )

QuestionForm = inlineformset_factory(
        Assignment,Question,exclude = ['test','order',],fk_name='test', max_num=10,extra=10,
        widgets={
        'ques':Textarea(attrs={'cols': 40, 'rows': 3}),
        'option1':Textarea(attrs={'cols': 25, 'rows': 1}),
        'option2':Textarea(attrs={'cols': 25, 'rows': 1}),
        'option3':Textarea(attrs={'cols': 25, 'rows': 1}),
        'option4':Textarea(attrs={'cols': 25, 'rows': 1}),
        }
    )