# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-26 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_customuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.CharField(
                default='', editable=False, max_length=1000),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
