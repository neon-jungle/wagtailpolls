# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpolls', '0002_remove_poll_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='issue_date',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='last_updated',
        ),
        migrations.AddField(
            model_name='poll',
            name='title',
            field=models.CharField(max_length=128, default=''),
            preserve_default=False,
        ),
    ]
