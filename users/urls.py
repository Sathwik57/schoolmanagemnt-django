from django.urls import path


from users.views import (
    Contactadd, HomePage, Profile,
    StudentAdd, StudentsList, 
    TeacherAdd, TeacherDelete, TeachersList, 
    UpdateStudent ,StudentDelete,TeacherUpdate
)


urlpatterns = [
    path('', HomePage.as_view(), name= 'home'),
    
    path('student/signup', StudentAdd.as_view(), name= 'add-student'),
    path('students/', StudentsList.as_view(), name= 'students'),
    path('students/<int:pk>/contact/', Contactadd.as_view(), name= 'contact-add'),
    path('students/<str:pk>/update/', UpdateStudent.as_view(), name= 'update-student'), 
    path('student/<str:pk>/delete/', StudentDelete.as_view(), name= 'delete-student'),

    path('teacher/signup', TeacherAdd.as_view(), name= 'add-teacher'),
    path('teachers/', TeachersList.as_view(), name= 'teachers'),
    path('teachers/<str:pk>/update', TeacherUpdate.as_view(), name= 'update-teacher'),
    path('teacher/<str:pk>/delete', TeacherDelete.as_view(), name= 'delete-teacher'),

    path('user-profile/<str:pk>', Profile.as_view(), name= 'profile'),
]