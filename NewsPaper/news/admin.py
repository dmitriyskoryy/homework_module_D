from django.contrib import admin
from .models import *


def send_message(modeladmin, request, queryset):
    print('Действия из админки')
    send_message.short_description = 'Вывести сообщение в консоль'  # описание для более понятного представления в админ панеле задаётся, как будто это объект


#создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('title', 'author',) # генерируем список имён всех полей для более красивого отображения

    actions = [send_message]  # добавляем действия в список



admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Subscriber)


