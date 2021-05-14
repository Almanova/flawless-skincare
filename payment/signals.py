from django.db.models.signals import post_save
from django.dispatch import receiver

from utils import constants
from .models import Payment


@receiver(post_save, sender=Payment)
def payment_post_save(sender, instance, **kwargs):
    if instance.status == constants.SUCCESS:
        instance.order.status = constants.CONFIRMED
        instance.order.save()
