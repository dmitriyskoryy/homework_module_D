from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, TextInput
from .models import *


# Создаём модельную форму
class NewsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].empty_label = "Автор не выбран"

    # в класс мета, как обычно, надо написать модель, по которой будет строиться форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'postCategory',]

        # widgets = {
        #     'title': TextInput(attrs={'class': 'form-input'}),
        # }

    #пользовательский валидатор
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 255:
            raise ValidationError('Длина заголовка не более 255 символов!')

        return title


