from django import template

# если мы не зарегестрируем наши фильтры, то django никогда не узнает где именно их искать и фильтры потеряются
register = template.Library()

unwanted_words = ['бля', 'хуй', 'хуе', 'хуё', 'хуи', 'пизд', 'пезд',
                   'пёзд', 'гандо', 'ебан', 'ебат', 'ебёт', 'ебл',
                   'ибат', 'ибет', 'ебу', 'ибу', 'ебал', 'ибал', 'залуп', 'салуп', 'выеб', 'выёб',
                   'ебиц', 'ёбиц', 'ебн', 'ёбн', 'ёб', 'аеб', 'оеб', 'аёб', 'оёб', 'пидо', 'педо', 'пиде',
                   'педе', 'уеб', 'уёб', 'иеб', 'иёб', 'гавн', 'ебаш', 'ибаш', 'ибош', 'ебош', 'какаш', 'срет',
                   'срёт', 'срит', 'срат', 'педик', 'гомик', 'клит', 'шлюх', 'жоп', 'говн', 'муда', 'муди', ]


# регистрируем наш фильтр под именем censor, чтоб django понимал, что это именно фильтр, а не простая функция
@register.filter(name='censor')
# первый аргумент здесь — это то значение, к которому надо применить фильтр
def censor(value):
    list_value = value.split()

    clear_list = []

    for word_list_value in list_value:
        flag = True
        word_lower = word_list_value.lower()
        for unwanted_word in unwanted_words:
            if unwanted_word in word_lower:
                s = f'{word_list_value[:1]}...{word_list_value[-1]}'
                word_list_value = s
                # flag = True
                break

        clear_list.append(word_list_value)

    return ' '.join(clear_list)












