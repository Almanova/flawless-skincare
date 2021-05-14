from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings

from .models import CustomerProfile, AdminProfile, Brand
from utils import constants


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == constants.CUSTOMER:
            CustomerProfile.objects.create(user=instance)
        elif instance.role == constants.ADMIN:
            AdminProfile.objects.create(user=instance)
        elif instance.role == constants.PARTNER:
            Brand.objects.create(user=instance)


@receiver(pre_delete, sender=settings.AUTH_USER_MODEL)
def delete_user_profile(sender, instance, **kwargs):
    if instance.role == constants.CUSTOMER:
        instance.customerprofile.delete()
    elif instance.role == constants.ADMIN:
        instance.adminprofile.delete()
    elif instance.role == constants.PARTNER:
        instance.brand.delete()
