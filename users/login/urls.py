from django.urls import path
from django.contrib.auth.views import (
    LoginView ,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordResetDoneView
    ) 
from django.views.generic import TemplateView


urlpatterns = [
    path('login/', LoginView.as_view(
        template_name = 'login.html',
        redirect_authenticated_user=True) ,name ='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('signup/', TemplateView.as_view(template_name ='signup.html'), name= 'signup'),

    path('reset_password/',PasswordResetView.as_view(template_name = 'reset_password.html'),
        name  = 'reset_password'),
    path('reset_password_sent/',PasswordResetDoneView.as_view(template_name = 'reset_password_sent.html'),
        name  = 'password_reset_done'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name = 'reset_password_confirm.html'),
        name  = 'password_reset_confirm'),
    path('reset_password_complete/',PasswordResetCompleteView.as_view(template_name = 'reset_password_complete.html'),
        name  = 'password_reset_complete'),    
]