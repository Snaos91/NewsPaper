from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .models import Post, Category


from celery import *
import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from collections import defaultdict

from django.conf import settings


@shared_task()
def notify_managers_posts(action, instance, pk_set):
    email_from = settings.DEFAULT_FROM_EMAIL
    if action == 'post_add':
        html_content = render_to_string(
            'new_post_email.html',
            {'post': instance, }
        )
        for pk in pk_set:
            category = Category.objects.get(pk=pk)
            recipients = [user.email for user in category.subscribers.all()]
            msg = EmailMultiAlternatives(
                subject=f'На сайте NewsPaper новая статья: {instance.title}',
                body=f'На сайте NewsPaper новая статья: {instance.title}',
                from_email=email_from,
                to=recipients
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


def send_posts(email_list, posts):
    # на случай, если там только один адрес, а не список
    if isinstance(email_list, str):
        subscriber_list = [email_list, ]
    else:
        subscriber_list = email_list

    email_form = settings.DEFAULT_FROM_EMAIL
    subject = 'В категориях, на которые вы подписаны появились новые статьи'
    text_message = 'В категориях, на которые вы подписаны появились новые статьи'

    # рендерим в строку шаблон письма и передаём туда переменные, которые в нём используем
    render_html_template = render_to_string('post_list_week.html', {'posts': posts, 'subject': subject})

    # формируем письмо
    msg = EmailMultiAlternatives(subject, text_message, email_form, list(subscriber_list))

    # прикрепляем html-шаблон
    msg.attach_alternative(render_html_template, 'text/html')
    # отправляем
    msg.send()


@shared_task()
def send_posts_to_email_weekly():

    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    last_week_posts_qs = Post.objects.filter(data_time_creation__gte=last_week)

    posts_for_user = defaultdict(set)  # user -> posts

    for post in last_week_posts_qs:
        for category in post.category.all():
            for user in category.subscribers.all():
                posts_for_user[user].add(post)

    # непосредственно рассылка
    for user, posts in posts_for_user.items():
        send_posts(user.email, posts)
