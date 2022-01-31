#  views.generic позволит выводить все объекты из БД в браузер "в HTML"
from django.shortcuts import render


from django.views import generic
from django.core.paginator import Paginator # импортируем класс, позволяющий удобно осуществлять постраничный вывод

#для того чтобы сделать декорированное представление с помощью миксина LoginRequiredMixin,
# которое будет выполняться если пользователь аутентифицирован на сайте
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
# класс для создание объекта письма с html
from django.core.mail import EmailMultiAlternatives
#  функция, которая срендерит  html в текст
from django.template.loader import render_to_string

from datetime import datetime

from .filters import PostFilter #My_AuthorFilter, My_DateFilter # импортируем написанный фильтр
from .models import *
from .forms import NewsForm
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


    # метод get_context_data нужен  для того, чтобы  передать переменные в шаблон.
    # В возвращаемом словаре context будут храниться все переменные. Ключи этого словаря и есть переменные,
    # к которым мы сможем потом обратиться через шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context





class PostDetailView(generic.DetailView):
    template_name = 'news_detail.html'
    context_object_name = 'new'
    queryset = Post.objects.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context




class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Post
    template_name = 'news_create.html'
    form_class = NewsForm
    permission_required = ('news.add_post',)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NewsForm()
        return context


    # при добавлении новости будет сообщать об этом на почту
    # получем html
    html_content = render_to_string(
        'mail_send.html',
        {
            'mynews': '()',
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'Письно при доб новости, {datetime.now()}',
        body='sdfsdfsdfsdf',
        from_email='di.sk39@yandex.ru',
        to=['progdebug39@gmail.com'],
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    # msg.send()  # отсылаем



    # send_mail(
    #     subject=f'Письно при доб новости, {datetime.now("%Y-%M-%d")}',
    #     message='Текс присьма',
    #     from_email='di.sk39@yandex.ru',  # почта, с которой отправлять
    #     recipient_list=['progdebug39@gmail.com', ],
    # )




class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Post
    template_name = 'news_create.html'
    form_class = NewsForm
    permission_required = ('news.change_post',)


    # метод get_object  исп вместо queryset, чтобы получить информацию об объекте который нужно редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)





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



@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')

    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news/')


# def user_search(request):
#     f = My_AuthorFilter(request.GET, queryset=User.objects.all())
#     return render(request, 'search.html', {'filter': f})
#
#
# def date_search(request):
#     d = My_DateFilter(request.GET, queryset=Post.objects.all())
#     return render(request, 'search.html', {'filter': d})