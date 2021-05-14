from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg, Sum

from auth_.models import Brand
from mixin.models import BaseModel, BaseManager
from utils import constants
from utils.uploads import product_upload


class Category(BaseModel):
    name = models.CharField(max_length=50,
                            verbose_name='Name')
    cashback = models.PositiveSmallIntegerField(default=0,
                                                validators=[MinValueValidator(0),
                                                            MaxValueValidator(100)],
                                                verbose_name='Cashback')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=200,
                            db_index=True,
                            verbose_name='Name')
    category = models.ForeignKey(Category,
                                 on_delete=models.PROTECT,
                                 related_name='products',
                                 verbose_name='Category')
    brand = models.ForeignKey(Brand,
                              on_delete=models.PROTECT,
                              related_name='products',
                              verbose_name='Brand')
    description = models.TextField(max_length=500,
                                   blank=True,
                                   null=True,
                                   verbose_name='Description')
    price = models.PositiveIntegerField(verbose_name='Original Price')
    discount = models.PositiveSmallIntegerField(default=0,
                                                validators=[MinValueValidator(0),
                                                            MaxValueValidator(100)],
                                                verbose_name='Discount')
    cashback = models.PositiveSmallIntegerField(default=0,
                                                validators=[MinValueValidator(0),
                                                            MaxValueValidator(100)],
                                                verbose_name='Cashback')
    weight = models.PositiveIntegerField(verbose_name='Weight')
    count = models.PositiveIntegerField(default=0,
                                        verbose_name='Amount of Product Available')
    order_count = models.PositiveIntegerField(default=0,
                                              verbose_name='Number of Times Ordered')
    rating = models.FloatField(blank=True,
                               null=True,
                               validators=[MinValueValidator(1.0),
                                           MaxValueValidator(5.0)],
                               verbose_name='Average Rating')

    class Meta:
        ordering = ['name', ]
        verbose_name = 'Product',
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    def recalculate_rating(self):
        self.rating = round(Review.objects
                            .filter(product=self, hidden=False)
                            .aggregate(average_rating=Avg('rating'))
                            ['average_rating'], 1)
        self.save()


class ProductImage(BaseModel):
    image = models.FileField(upload_to=product_upload,
                             verbose_name='Image')
    priority = models.PositiveSmallIntegerField(blank=True,
                                                null=True,
                                                verbose_name='Priority')
    product = models.ForeignKey(Product,
                                on_delete=models.PROTECT,
                                related_name='images',
                                verbose_name='Product')

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'


class CartItem(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='cart_items',
                             verbose_name='User')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='cart_items',
                                verbose_name='Product')
    quantity = models.PositiveIntegerField(default=1,
                                           verbose_name='Quantity')

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Review(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.DO_NOTHING,
                             related_name='reviews',
                             verbose_name='User')
    product = models.ForeignKey(Product,
                                on_delete=models.DO_NOTHING,
                                related_name='reviews',
                                verbose_name='Product')
    rating = models.PositiveSmallIntegerField(default=5,
                                              validators=[MinValueValidator(1),
                                                          MaxValueValidator(5)],
                                              verbose_name='Rating')
    comment = models.TextField(blank=True,
                               null=True,
                               verbose_name='Review')

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f"{self.user.username}: {self.product.name} - {self.comment}"


class Favourite(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='favourites',
                             verbose_name='User')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='favourites',
                                verbose_name='Product')

    class Meta:
        verbose_name = 'Favourite'
        verbose_name_plural = 'Favourites'

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Order(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.DO_NOTHING,
                             related_name='orders',
                             verbose_name='User')
    address = models.CharField(max_length=200,
                               verbose_name='Delivery Address')
    status = models.CharField(choices=constants.ORDER_STATUSES,
                              default=constants.WAITING,
                              max_length=50,
                              verbose_name='Status')
    price = models.PositiveIntegerField(null=True,
                                        blank=True,
                                        verbose_name='Original Price')
    discounted_price = models.FloatField(null=True,
                                         blank=True,
                                         verbose_name='Price with Discount')
    delivery_price = models.FloatField(null=True,
                                       blank=True,
                                       verbose_name='Delivery Price')
    total_price = models.FloatField(null=True,
                                    blank=True,
                                    verbose_name='Total Price')
    cashback = models.FloatField(null=True,
                                 blank=True,
                                 verbose_name='Cashback')

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"{self.user.username} - {self.total_price}"

    def calculate_price(self):
        self.price = self.order_items.aggregate(
            price=Sum('price'))['price']
        self.discounted_price = self.order_items.aggregate(
            discounted_price=Sum('total_price'))['discounted_price']
        self.delivery_price = constants.DELIVERY_PRICE if \
            self.discounted_price < constants.FREE_DELIVERY_MIN_PRICE else 0
        self.total_price = self.discounted_price + self.delivery_price
        self.cashback = self.order_items.aggregate(
            cashback=Sum('cashback'))['cashback']
        self.save()


class OrderItemManager(BaseManager):
    def add_to_order(self, order, cart_items):
        for cart_item in cart_items:
            total_price = (cart_item.product.price -
                           cart_item.product.price *
                           cart_item.product.discount * 0.01) \
                          * cart_item.quantity
            cashback = total_price * \
                       cart_item.product.cashback * 0.01
            order_item = self.model(order=order,
                                    product=cart_item.product,
                                    quantity=cart_item.quantity,
                                    price=cart_item.product.price * cart_item.quantity,
                                    discount=cart_item.product.discount,
                                    total_price=total_price,
                                    cashback=cashback)
            order_item.save()
        return order_item


class OrderItem(BaseModel):
    order = models.ForeignKey(Order,
                              on_delete=models.DO_NOTHING,
                              related_name='order_items',
                              verbose_name='Order')
    product = models.ForeignKey(Product,
                                on_delete=models.DO_NOTHING,
                                related_name='order_items',
                                verbose_name='Product')
    quantity = models.PositiveIntegerField(default=1,
                                           verbose_name='Quantity')
    price = models.PositiveIntegerField(verbose_name='Original Price')
    discount = models.PositiveSmallIntegerField(default=0,
                                                verbose_name='Discount')
    total_price = models.FloatField(verbose_name='Total Price')
    cashback = models.FloatField(verbose_name='Cashback')

    objects = OrderItemManager()

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
