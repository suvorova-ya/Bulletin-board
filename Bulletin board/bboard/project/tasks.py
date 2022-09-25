from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, User
import datetime
from django.conf import settings

@shared_task
def weekly_mailing_list():
    new_post = Post.objects.filter(created__gt=(datetime.date.today() - datetime.timedelta(days=7)))
    if new_post:
        post_list = str(new_post)
        for user in User.objects.all():
            msg = EmailMultiAlternatives(
                subject="Новые объявления за неделю",
                body=post_list,
                from_email= settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            html_content = render_to_string(
                'project/mailing_list.html',
                {
                    'posts': new_post,
                    'recipient': user.username
                }
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


            print('Уведомление отослано подписчику ', user.username, ' на тему ', post_list)