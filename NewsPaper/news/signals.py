from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category


@receiver(post_save, sender=Post)
def save_post(sender, **kwargs):
    post_instance = kwargs['instance']
    subscribers_list = {user.email
                        for category in post_instance.category.all()
                        for user in category.subscribers.all()}

    email_from = settings.DEFAULT_FROM_EMAIL

    subject = 'Новая статья'
    text_message = 'Новая статья'
    render_html_template = render_to_string('new_post_email.html')

    msg = EmailMultiAlternatives(subject, text_message, email_from, list(subscribers_list))
    msg.attach_alternative(render_html_template, 'text/html')
    msg.send()
