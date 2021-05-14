from django.contrib import admin
from .models import Category, Product, Review, \
    Favourite, OrderItem, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cashback')
    list_filter = ('cashback', 'created')
    search_fields = ('name', )


@admin.register(Product)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'discount', 'rating')
    list_filter = ('category', 'discount', 'created', 'rating')
    search_fields = ('name', 'category')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rating', 'created')
    list_filter = ('user', 'product', 'rating')
    search_fields = ('user', 'product')


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product')
    list_filter = ('user', 'product')
    search_fields = ('user', 'product')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'price')
    list_filter = ('order', )
    search_fields = ('order', 'product')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price')
    list_filter = ('user', 'total_price')
    search_fields = ('user', )
