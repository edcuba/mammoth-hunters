# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 17:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20171201_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='text',
            field=models.TextField(default=' '),
        ),
    ]
