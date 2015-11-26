# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpolls', '0003_auto_20151126_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 26, 22, 37, 42, 67129, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
