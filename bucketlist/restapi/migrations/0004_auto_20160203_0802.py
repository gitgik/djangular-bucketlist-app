# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-03 08:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0003_auto_20160203_0713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucketlist',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='bucketlistitem',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]