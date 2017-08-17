# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-16 02:14
from __future__ import unicode_literals

from django.conf import settings
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0004_auto_20170815_2020'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='media',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\ASUS\\Documents\\python_work\\Web Application\\dm\\static_cdn\\protected'), upload_to=products.models.download_media_location),
        ),
        migrations.AddField(
            model_name='myproducts',
            name='products',
            field=models.ManyToManyField(blank=True, to='products.Product'),
        ),
        migrations.AddField(
            model_name='myproducts',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]