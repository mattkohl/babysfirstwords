# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-10 08:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lists', '0002_list_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='shared_with',
            field=models.ManyToManyField(blank=True, related_name='shares_list', to=settings.AUTH_USER_MODEL),
        ),
    ]