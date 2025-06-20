# Generated by Django 5.2 on 2025-05-16 13:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0014_alter_product_picture'),
        ('cart', '0013_remove_cart_session_key_alter_cart_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='session_key',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.product'),
        ),
    ]
