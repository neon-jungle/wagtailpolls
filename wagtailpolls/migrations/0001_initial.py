# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('issue_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Issue date')),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
