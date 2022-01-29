from django import template

# если мы не зарегестрируем наши фильтры, то django никогда не узнает где именно их искать и фильтры потеряются
register = template.Library()

unwanted_words = ['негодяй', 'подонок', 'морд']


# регистрируем наш фильтр под именем censor, чтоб django понимал, что это именно фильтр, а не простая функция
@register.filter(name='censor')
# первый аргумент здесь — это то значение, к которому надо применить фильтр
def censor(value):
    list_value = value.split()

    clean_list = []

    for word_list_value in list_value:
        word_lower = word_list_value.lower()
        for unwanted_word in unwanted_words:
            if unwanted_word in word_lower:
                s = f'{word_list_value[:1]}...{word_list_value[-1]}'
                word_list_value = s
                break

        clean_list.append(word_list_value)

    return ' '.join(clean_list)












