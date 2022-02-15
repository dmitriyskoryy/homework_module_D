from django.urls import path
from .views import *

from django.views.decorators.cache import cache_page

#можно делать не через path, а через url


urlpatterns = [
    path('', PostList.as_view()), # as_view говорит что представление PostList, будет представлен ввиде представления
    path('<int:pk>/', PostDetailView.as_view(), name='news_detail'),
    # path('<int:pk>/', cache_page(20)(PostDetailView.as_view()), name='news_detail'), кэширование для дженерика
    path('news_create/', PostCreateView.as_view(), name='news_create'),
    path('news_create/<int:pk>/', PostUpdateView.as_view(), name='news_update'),
    path('news_delete/<int:pk>/', PostDeleteView.as_view(), name='news_delete'),
    path('search/', PostSearch.as_view()),

    path('upgrade/', upgrade_me, name='upgrade'),
    path('subscribe/', subscribe_me, name='subscribe'),


    # path('search/', user_search),
    # path('search/', date_search),

]