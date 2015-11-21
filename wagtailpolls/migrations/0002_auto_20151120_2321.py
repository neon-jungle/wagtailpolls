# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpolls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('ip', models.GenericIPAddressField()),
                ('choice', models.ForeignKey(to='wagtailpolls.Question')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('ip', 'choice')]),
        ),
    ]
