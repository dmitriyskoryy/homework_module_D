from datetime import datetime, timedelta
import logging

from datetime import timezone
from smtplib import SMTPDataError

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
# from django_apscheduler.jobstores import DjangoJobStore
# from django_apscheduler.models import DjangoJobExecution


from ...models import *

logger = logging.getLogger(__name__)


def my_job():
    #получаем все категории новостей
    all_categoryes = [cat.name for cat in Category.objects.all()]

    # OurTZ = pytz.timezone('Europe/Kaliningrad')
    datestart = datetime.now() - timedelta(days=2)

    for cat in all_categoryes:
        #получаем все новости категории (cat) за определенный период
        post = Post.objects.filter(dateCreation__range=[datestart, datetime.now()], postCategory=Category.objects.get(name=cat))


        #теперь получить email подписчиков категорий
        list_email_subscriptions = [em.subscribersUser.email for em in
                                      Subscriber.objects.filter(postCategory=Category.objects.get(name=cat))]


        # и отправить им новости за период
        if list_email_subscriptions:
            for email in list_email_subscriptions:
                html_content = render_to_string(
                    'send_week_news.html',
                    {
                        'news': post,
                        'email': email,
                    }
                )

                msg = EmailMultiAlternatives(
                    subject=f'Здравствуй. Твои любимые новости и статьи на портале NewsPaper!',
                    body=f'Это автоматическая рассылка.',
                    from_email=f'dnetdima@gmail.com',
                    to=[email, ],
                )
                msg.attach_alternative(html_content, "text/html")

                try:
                    #msg.send()
                    print('send')
                except:
                    raise SMTPDataError(554, 'Сообщение отклонено по подозрению в спаме!')

# datetime.strftime(datetime.now(), '%d.%m.%Y')

# python manage.py runapscheduler



# функция которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    # DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        # scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day="*/7"), #интервал
            # Тоже самое что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True, #задача будет заменяться
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")