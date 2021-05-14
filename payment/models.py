from django.db import models

from core.models import Order
from mixin.models import BaseModel
from utils import constants


class Payment(BaseModel):
    order = models.OneToOneField(Order,
                                 on_delete=models.DO_NOTHING,
                                 related_name='payment',
                                 verbose_name='Order')
    status = models.CharField(choices=constants.PAYMENT_STATUSES,
                              default=constants.WAITING,
                              max_length=50,
                              verbose_name='Status')
    transaction = models.TextField(max_length=1000,
                                   blank=True,
                                   null=True,
                                   verbose_name='Transaction Log')

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f"{self.order.user.username} - {self.status}"
