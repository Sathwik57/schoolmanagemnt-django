from django.contrib import admin
from users.models import Student, Teacher, User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('combine','first_name' , 'email' , 'username' ,'is_student')
    list_display_links = ('combine',)
    list_editable = ('username',)

    def combine(self,obj):
        return f'{obj.first_name} {obj.last_name}({obj.username})'

class StudentAdmin(admin.ModelAdmin):
    list_display = ('combine','user' , 'rollno' , 'std')
    list_display_links = ('combine',)
    list_editable = ( 'rollno' , 'std',)

    def combine(self,obj):
        return f'{obj.user}-{obj.rollno}'

admin.site.register( User , UserAdmin)
admin.site.register(Teacher)
admin.site.register(Student , StudentAdmin)