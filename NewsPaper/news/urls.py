from django.urls import path
from .views import PostList, PostDetail


urlpatterns = [
    path('', PostList.as_view()), # as_view говорит что представление PostList, будет представлен ввиде представления
    path('<int:pk>', PostDetail.as_view())
]