
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('news.urls')),# делаем так, чтобы все адреса из приложения (news/urls.py) сами автоматически подключались когда мы их добавим.
    path('accounts/', include('allauth.urls')),
]
