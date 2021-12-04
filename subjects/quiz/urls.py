from django.urls import path
from .views import  QuizList,TakeQuiz,Results,ResultsList 


urlpatterns = [
    path('',QuizList.as_view(),name = 'quiz'), 
    path('<int:pk>/takequiz',TakeQuiz.as_view(),name = 'take-quiz'),     
    path('<int:pk>/result',Results.as_view(),name = 'quiz-result'),
    path('student/<int:pk>/results',ResultsList.as_view(),name = 'results'), 
]