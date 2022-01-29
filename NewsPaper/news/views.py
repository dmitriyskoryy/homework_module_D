#  views.generic позволит выводить все объекты из БД в браузер "в HTML"
from django.shortcuts import render


from django.views import generic
from django.core.paginator import Paginator # импортируем класс, позволяющий удобно осуществлять постраничный вывод

#для того чтобы сделать декорированное представление с помощью миксина LoginRequiredMixin,
# которое будет выполняться если пользователь аутентифицирован на сайте
from django.contrib.auth.mixins import LoginRequiredMixin


from datetime import datetime

from .filters import PostFilter #My_AuthorFilter, My_DateFilter # импортируем написанный фильтр
from .models import *
from .forms import NewsForm # импортируем  форму
from django.contrib.auth.models import User


# пишем представление
class PostList(generic.ListView):
    # указываем модель, объекты которой будем выводить
    model = Post
    # указываем имя шаблона, в котором будет лежать html, в котором будут все инструкции о том,
    # как именно пользователю должны вывеститсь наши объекты
    template_name = 'news_list.html'
    # это имя списка, в котором будут лежать все объекты, его надо указать,
    # чтобы обратиться к самоу списку объектов через html-шаблон
    context_object_name = 'newslist'
    ordering = ['-id']
    paginate_by = 6


    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон.
    # В возвращаемом словаре context будут храниться все переменные. Ключи этого словаря и есть переменные,
    # к которым мы сможем потом обратиться через шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        return context




# дженерик для получения деталей о товаре
class PostDetailView(generic.DetailView):
    template_name = 'news_detail.html'
    context_object_name = 'new'
    queryset = Post.objects.all()



# дженерик для создания объекта. Надо указать только имя шаблона и класс формы . Остальное он сделает сам
class PostCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'news_create.html'
    form_class = NewsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NewsForm()
        return context





# дженерик для редактирования объекта
class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'news_create.html'
    form_class = NewsForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления
class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'



# пишем представление
class PostSearch(generic.ListView):
    # указываем модель, объекты которой будем выводить
    model = Post
    # указываем имя шаблона, в котором будет лежать html, в котором будут все инструкции о том,
    # как именно пользователю должны вывеститсь наши объекты
    template_name = 'search.html'
    # это имя списка, в котором будут лежать все объекты, его надо указать,
    # чтобы обратиться к самоу списку объектов через html-шаблон
    context_object_name = 'search'
    ordering = ['-id']


    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    #*args это кортеж, а **kwargs это словарь
    #**super() это распаковка именованных аргументов
    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            "filter": self.get_filter(),
        }

        #context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        #return context

#
# def user_search(request):
#     f = My_AuthorFilter(request.GET, queryset=User.objects.all())
#     return render(request, 'search.html', {'filter': f})
#
#
# def date_search(request):
#     d = My_DateFilter(request.GET, queryset=Post.objects.all())
#     return render(request, 'search.html', {'filter': d})