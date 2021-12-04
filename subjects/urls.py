from django.urls import path


from subjects.views import (
    AddAssignment,
    AddQuestions,
    AssignmentDetail,
    UpdateAssignment,
    DeletetAssignments,
    UpdateQuestion,
    DelQuestion,
    GradedList
)


urlpatterns = [
    path('assignments/add',AddAssignment.as_view(),name='add-assignment'),
    path('assignment/<int:pk>',AssignmentDetail.as_view(),name='assignment-detail'),
    path('assignment/<int:pk>/update',UpdateAssignment.as_view(),name='assignment-update'),  
    path('assignment/<int:pk>/delete',DeletetAssignments.as_view(),name='assignment-delete'),  

    path('assignment/<int:pk>/ques/add',AddQuestions.as_view(),name='add-ques'),
    path('assignment/<int:pk>/ques/update',UpdateQuestion.as_view(),name='ques-update'),
    path('assignment/ques/<int:pk>/delete',DelQuestion.as_view(),name='ques-delete'),

    path('assignments/results',GradedList.as_view(),name='graded-list'),
    
]
