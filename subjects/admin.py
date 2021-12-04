from django.contrib import admin

from subjects.models import (
    Subject,Assignment,
    Question,
    GradedAssignment    
    )

# Register your models here.

admin.site.register(Subject)
admin.site.register(Assignment)
admin.site.register(Question)
admin.site.register(GradedAssignment)