from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from payment.models import Payment
from .models import Review, Order, OrderItem, CartItem


@receiver(post_save, sender=Review)
def review_post_save(sender, instance, **kwargs):
    instance.product.recalculate_rating()


@receiver(pre_delete, sender=Review)
def review_post_delete(sender, instance, **kwargs):
    instance.product.recalculate_rating()


@receiver(post_save, sender=Order)
def order_post_save(sender, instance, **kwargs):
    if instance.total_price is None:
        OrderItem.objects.add_to_order(
            instance, CartItem.objects.filter(user=instance.user))
        instance.calculate_price()
        Payment.objects.create(order=instance)
