# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-27 17:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.RenameField(
            model_name='bucketlist',
            old_name='user',
            new_name='created_by',
        ),
        migrations.RenameField(
            model_name='bucketlistitem',
            old_name='user',
            new_name='created_by',
        ),
        migrations.AlterField(
            model_name='bucketlist',
            name='date_modified',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='bucketlist',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='bucketlistitem',
            name='bucketlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='restapi.Bucketlist'),
        ),
        migrations.AlterField(
            model_name='bucketlistitem',
            name='date_modified',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='bucketlistitem',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
