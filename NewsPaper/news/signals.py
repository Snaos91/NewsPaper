from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category


@receiver(m2m_changed, sender=Post.category.through)
def notify_managers_posts(instance, action, pk_set, *args, **kwargs):
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
