# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpolls', '0002_auto_20151120_2321'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='question',
            field=modelcluster.fields.ParentalKey(to='wagtailpolls.Question', default='', related_name='votes'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='vote',
            name='choice',
        ),
    ]
