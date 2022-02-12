from smtplib import SMTPDataError

from allauth.account.signals import user_signed_up
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

#  функция, которая срендерит  html в текст
from django.template.loader import render_to_string
# класс для создание объекта письма с html
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail

from .models import *


# # в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(m2m_changed, sender=Post.postCategory.through)
def notify_users_news(sender, instance, action, **kwargs):

    if action == "post_add":
        post = Post.objects.get(pk=instance.id)
        categoryes = [s.name for s in post.postCategory.all()]

        if categoryes:
            for cat in categoryes:
                list_email_subscriptions = [d.subscribersUser.email for d in Subscriber.objects.filter(postCategory=Category.objects.get(name=cat))]


            if list_email_subscriptions:
                for email in list_email_subscriptions:
                    html_content = render_to_string(
                        'mail_send.html',
                        {
                            'new': post,
                            'email': email,
                        }
                    )

                    msg = EmailMultiAlternatives(
                        subject=f'Здравствуй. Новая статья в твоём любимом разделе!',
                        body=f'Это автоматическая рассылка.',
                        from_email=f'dnetdima@gmail.com',
                        to=[email,],
                    )
                    msg.attach_alternative(html_content, "text/html")

                    try:
                        print('send')
                        #msg.send()
                    except:
                        raise SMTPDataError(554, 'Сообщение отклонено по подозрению в спаме!')

        # send_mail(
        #     subject=f'Здравствуй. Новая статья в твоём любимом разделе!',
        #     message='Текс присьма',
        #     from_email='dnetdima@gmail.com',
        #     recipient_list=list_email_subscriptions,
        # )


   # # отправляем письмо всем админам по аналогии с send_mail, только здесь получателя указывать не надо
    # mail_admins(
    #     subject=f'{content.title}, дата: {datetime.now().strftime("%d/%m/%y")}',
    #     message='content',
    # )


# @receiver(post_save, sender=Post)
# def save_post(sender, instance, created, **kwargs):
#     def save(self, *args, **kwargs):
#         user = self.request.user
#         f = Post.objects.filter(author=user)
#         print(f, ' ====================================================')
#         # if self.request.user:
#         #     raise ValueError("Updating the value of creator isn't allowed")
#         super().save(*args, **kwargs)




#сигнал при регистрации на портале
@receiver(user_signed_up, dispatch_uid="some.unique.string.id.for.allauth.user_signed_up")
def user_signed_up_(request, user, **kwargs):
    send_mail(
        subject=f'Регистрация на портале NewsPortal.',
        message=f'Добро пожаловать {user}. Ваша регистрация на NewsPortal прошла успешно!',
        from_email='dnetdima@gmail.com',
        recipient_list=[user.email],
    )