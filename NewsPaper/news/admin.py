from django.contrib import admin
from .models import *


#создаём новый класс для представления товаров в админке
# class PostAdmin(admin.ModelAdmin):
#     # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
#     list_display = [field.name for field in Category._meta.get_fields()] # генерируем список имён всех полей для более красивого отображения
#


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Subscriber)


