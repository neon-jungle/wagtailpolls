# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.fields
import django.utils.timezone
import wagtail.wagtailsearch.index


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, wagtail.wagtailsearch.index.Indexed),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=128)),
                ('poll', modelcluster.fields.ParentalKey(to='wagtailpolls.Poll', related_name='questions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('ip', models.GenericIPAddressField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('question', modelcluster.fields.ParentalKey(to='wagtailpolls.Question', related_name='votes')),
            ],
        ),
    ]
