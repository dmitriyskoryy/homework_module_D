from django.db import models

#User импортируется из django.contrib.auth.models
from django.contrib.auth.models import User

from django.db.models import Sum

from django.core.cache import cache

class Author(models.Model):
    #Взять один ко дному Автора и Юзера
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)


    def __str__(self):
        return f'{self.authorUser.username}'

    # с помощью post_set.all() получаем все связанные посты
    # метод aggregate служит для работы с множеством записей
    # создаем значение postRating, куда присваиваем сумму всех значений поля rating
    def update_rating(self):
        postRat = self.post_set.all().aggregate(postRating=Sum('rating'))
        pRat = 0
        #получаем сумму поля rating связанного с автором
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.all().aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()



class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.name}'



class Post(models.Model):
    #связь один ко многим с моделью Author
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Author')

    NEWS = 'NW'
    ARTICLE = 'AR'

    CATEGORY_CHOICES = (
        (NEWS, 'News'),
        (ARTICLE, 'Article'),
    )

    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=NEWS, verbose_name='TypeNews')

    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Date')

    # связь многие ко многим с моделью Category, through - промежуточная модель PostCategory
    postCategory = models.ManyToManyField(Category, through='PostCategory', verbose_name='Category')


    title = models.CharField(max_length=128, verbose_name='Caption')
    text = models.TextField(verbose_name='Text post')
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.author.authorUser.username} {self.postCategory.name}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

    #добавим ссылку на текущий объект. Для того, чтобы при создании объекта или переходе
    #к его деталям не прописывать в каждом дженерике succes_url.
    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с новостю
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его




    # промежуточная модель
class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)



class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)

    # комментарии могут оставлять все, поэтому связь с User, а не с Author
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    # добираеся с помощью длинной связи до имени юзера (автора) который написал комментарий
    def __str__(self):
        try:
            return self.commentPost.author.authorUser.username
        except:
            return self.commentUser.username


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()



class Subscriber(models.Model):
    subscribersUser = models.ForeignKey(User, on_delete=models.CASCADE)
    postCategory = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.subscribersUser} {self.postCategory}'

