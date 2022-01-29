from django.urls import path
from .views import *

#можно делать не через path, а через url


urlpatterns = [
    path('', PostList.as_view()), # as_view говорит что представление PostList, будет представлен ввиде представления
    path('<int:pk>/', PostDetailView.as_view(), name='news_detail'), # Ссылка на детали новости
    path('news_create/', PostCreateView.as_view(), name='news_create'),# Ссылка на создание новости
    path('news_create/<int:pk>/', PostUpdateView.as_view(), name='news_update'),# Ссылка на изменение новости
    path('news_delete/<int:pk>/', PostDeleteView.as_view(), name='news_delete'),# Ссылка на уладение новости
    path('search/', PostSearch.as_view()),


    # path('search/', user_search),
    # path('search/', date_search),

]