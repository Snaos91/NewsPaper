from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category
from .tasks import notify_managers_posts


@receiver(m2m_changed, sender=Post.category.through)
def create_post(instance, action, pk_set, *args, **kwargs):
    notify_managers_posts(instance.pk, action, pk_set)
