from django.db.models.signals import pre_save
from django.dispatch import receiver

from blog.models import Blog


@receiver(pre_save, sender=Blog)
def set_paid_status(sender, instance, **kwargs):
    if instance.owner.subscription.is_subscribed:
        instance.is_paid = True
    else:
        instance.is_paid = False
