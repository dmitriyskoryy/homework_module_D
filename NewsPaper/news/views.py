#  views.generic позволит выводить все объекты из БД в браузер "в HTML"
from django.views.generic import ListView, DetailView
from .models import *

# пишем представление
class PostList(ListView):
    # указываем модель, объекты которой будем выводить
    model = Post
    # указываем имя шаблона, в котором будет лежать html, в котором будут все инструкции о том,
    # как именно пользователю должны вывеститсь наши объекты
    template_name = 'newsall.html'
    # это имя списка, в котором будут лежать все объекты, его надо указать,
    # чтобы обратиться к самоу списку объектов через html-шаблон
    context_object_name = 'newsall'



class PostDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'