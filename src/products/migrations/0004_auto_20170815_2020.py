# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-15 12:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to=products.models.download_media_location),
        ),
        migrations.AlterField(
            model_name='product',
            name='managers',
            field=models.ManyToManyField(blank=True, related_name='managers_products', to=settings.AUTH_USER_MODEL),
        ),
    ]
