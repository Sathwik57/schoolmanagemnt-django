from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.login.urls')),

    path('', include('users.urls')),
    path('subjects/', include('subjects.urls')),
    path('quiz/', include('subjects.quiz.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL ,document_root = settings.MEDIA_ROOT)