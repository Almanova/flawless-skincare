from django.contrib import admin
from .models import User, AdminProfile, CustomerProfile, Brand


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'created')
    list_filter = ('created', 'is_staff', 'is_active', 'hidden')
    search_fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'position')
    list_filter = ('position', 'created')
    search_fields = ('user', 'position')


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'city')
    list_filter = ('city', 'created', 'birth_date')
    search_fields = ('user', 'city', 'address')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name')
    list_filter = ('user', 'created')
    search_fields = ('user', 'name', 'description')
