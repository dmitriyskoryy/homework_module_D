from django.core.exceptions import ObjectDoesNotExist
from django.views import generic
from django.core.paginator import Paginator # импортируем класс, позволяющий удобно осуществлять постраничный вывод

#для того чтобы сделать декорированное представление с помощью миксина LoginRequiredMixin,
# которое будет выполняться если пользователь аутентифицирован на сайте
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required






from datetime import datetime, timedelta

from .filters import PostFilter #My_AuthorFilter, My_DateFilter # импортируем написанный фильтр
from .models import *
from .forms import FormCreateNews
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
        user = self.request.user
        context['is_not_authors'] = not user.groups.filter(name='authors').exists()

        datestart = datetime.now() - timedelta(days=1)
        # получаем все новости за определенный период
        number_news = 0
        try:
            post = Post.objects.filter(dateCreation__range=[datestart, datetime.now()],
                                       author=Author.objects.get(authorUser=user))
            if post:
                number_news = len(post)
            else:
                number_news = 0
        except:
            print('Ошибка!')

        context['limit_news_author'] = number_news
        return context





class PostDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'news_detail.html'
    context_object_name = 'new'
    queryset = Post.objects.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        id = self.kwargs.get('pk')
        post = Post.objects.get(pk=id)


        # получаем все категории на которые уже подписан юзер
        user_subscriptions = [s.postCategory.name for s in Subscriber.objects.filter(subscribersUser=user)]

        # отбираем категории на которые не подписать юзер
        categoryes = {s.name for s in post.postCategory.all()}
        diff_set = categoryes.difference(user_subscriptions)
        context['diff_set'] = diff_set
        return context





class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Post
    template_name = 'news_create.html'
    form_class = FormCreateNews
    permission_required = ('news.add_post',)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FormCreateNews
        return context





class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Post
    template_name = 'news_create.html'
    form_class = FormCreateNews
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
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    ordering = ['-id']


    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

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
        Author.objects.create(authorUser=User.objects.get(username=user))
    return redirect('/news/')



@login_required
def subscribe_me(request):
    if request.method == "POST":
        user = request.user
        id_news = request.POST['id_news']
        post = Post.objects.get(pk=id_news)


        categoryes = set()
        # получаем все категории на которые хочет подписаться юзер, и формируем множество
        for s in post.postCategory.all():
            if request.POST.get(s.name):
                categoryes.add(request.POST.get(s.name))

        # categoryes = {s.name for s in post.postCategory.all()}

        if categoryes:
            #получаем все категории на которые уже подписан юзер, и формируем множество
            user_subscriptions = {s.postCategory.name for s in Subscriber.objects.filter(subscribersUser=user)}
            #отбираем категории на которые не подписать юзер
            diff_set = categoryes.difference(user_subscriptions)

            #добавляем категории для юзера в таблицу Subscriber
            if diff_set:
                for cat in diff_set:
                    Subscriber.objects.create(subscribersUser=User.objects.get(username=user), postCategory=Category.objects.get(name=cat))


        return redirect(f'/news/{id_news}')



# def user_search(request):
#     f = My_AuthorFilter(request.GET, queryset=User.objects.all())
#     return render(request, 'search.html', {'filter': f})
#
#
# def date_search(request):
#     d = My_DateFilter(request.GET, queryset=Post.objects.all())
#     return render(request, 'search.html', {'filter': d})