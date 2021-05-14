# Generated by Django 3.2 on 2021-05-14 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_order_orderitem'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='transaction',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Transaction Log'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='payment', to='core.order', verbose_name='Order'),
        ),
    ]