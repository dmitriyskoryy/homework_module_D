from django_filters import FilterSet, CharFilter, DateFilter, ModelMultipleChoiceFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post, Author


# создаём фильтр
class PostFilter(FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т.е. подбираться) информация о новостях

    # author = ModelMultipleChoiceFilter('author',
    #     label ='Автор: ',
    #     lookup_expr ='exact',
    #     queryset=Author.objects.all(),
    # )
    # dateCreation = DateFilter('dateCreation',
    #     label ='Дата: ',
    #     lookup_expr ='gt',
    # )
    #
    # fields = {'author', 'dateCreation',}

    class Meta:
        model = Post
        fields = {
            'author': ['in'],
            'dateCreation': ['gt'],
        }

        #postCategory__name - таким образом, через __ мы обращаемся к полям связанного объекта
        # 'text': ['icontains'],
        #'dateCreation': ['gt'],  # дата создания должна быть больше или равна той, что указал пользователь
        # 'dateCreation': ['lt'],  # дата создания должна быть меньше или равнa той, что указал пользователь

#
#
# class My_AuthorFilter(FilterSet):
#     authorUser = CharFilter(method='user_filter')
#     class Meta:
#         model = Author
#         fields = ['authorUser']
#
#     def user_filter(self, queryset, name, value):
#         return queryset.filter(**{
#             name: value
#         })
#
#
# class My_DateFilter(FilterSet):
#     dateCreation = DateFilter()
#     class Meta:
#         model = Post
#         fields = ['dateCreation']

# class DataFilter(FilterSet):
#     date = DateFromToRangeFilter()
#     class Meta:
#         model = Post
#         fields = ['dateCreation']


# Ещё есть вариант - создавать фильтры не через class Meta, а напрямую - поля в классе PostFilter задавать статически:
#     title = CharFilter(‘title’,
#                                label=‘Заголовок содержит:’,
#                                lookup_expr=‘icontains’,
#                                )
#     author = ModelMultipleChoiceFilter(‘author’,
#                                label=‘Автор:’,
#                                lookup_expr=‘exact’,
#                                queryset=Author.objects.all()
#                                 )