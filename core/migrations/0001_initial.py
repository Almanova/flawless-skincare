# Generated by Django 3.2 on 2021-05-11 13:48

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import utils.uploads


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth_', '0004_user_confirmed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(db_index=True, editable=False, verbose_name='Created at')),
                ('modified', models.DateTimeField(db_index=True, verbose_name='Last modified')),
                ('hidden', models.BooleanField(db_index=True, default=False, verbose_name='Hidden or deleted')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('cashback', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Cashback')),
            ],
            options={
                'verbose_name': 'Cashback',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(db_index=True, editable=False, verbose_name='Created at')),
                ('modified', models.DateTimeField(db_index=True, verbose_name='Last modified')),
                ('hidden', models.BooleanField(db_index=True, default=False, verbose_name='Hidden or deleted')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='Name')),
                ('description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Description')),
                ('price', models.PositiveIntegerField(verbose_name='Original Price')),
                ('discount', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Discount')),
                ('cashback', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Cashback')),
                ('weight', models.PositiveIntegerField(verbose_name='Weight')),
                ('count', models.PositiveIntegerField(default=0, verbose_name='Amount of Product Available')),
                ('rating', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Average Rating')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='auth_.brand', verbose_name='Brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='core.category', verbose_name='Category')),
            ],
            options={
                'verbose_name': ('Product',),
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(db_index=True, editable=False, verbose_name='Created at')),
                ('modified', models.DateTimeField(db_index=True, verbose_name='Last modified')),
                ('hidden', models.BooleanField(db_index=True, default=False, verbose_name='Hidden or deleted')),
                ('image', models.FileField(upload_to=utils.uploads.product_upload, verbose_name='Image')),
                ('priority', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Priority')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='images', to='core.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Product Image',
                'verbose_name_plural': 'Product Images',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(db_index=True, editable=False, verbose_name='Created at')),
                ('modified', models.DateTimeField(db_index=True, verbose_name='Last modified')),
                ('hidden', models.BooleanField(db_index=True, default=False, verbose_name='Hidden or deleted')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='core.product', verbose_name='Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Cart Item',
                'verbose_name_plural': 'Cart Items',
                'unique_together': {('user', 'product')},
            },
        ),
    ]
