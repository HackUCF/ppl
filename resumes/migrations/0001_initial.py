# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-17 06:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('membership', '0001_initial'),
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('url', models.URLField(unique=True)),
                ('graduation', models.DateTimeField(choices=[(datetime.datetime(2015, 12, 18, 5, 0, tzinfo=utc), 'Fall 2015'), (datetime.datetime(2015, 5, 5, 4, 0, tzinfo=utc), 'Spring 2016'), (datetime.datetime(2015, 8, 6, 4, 0, tzinfo=utc), 'Summer 2016'), (datetime.datetime(2016, 12, 18, 5, 0, tzinfo=utc), 'Fall 2016'), (datetime.datetime(2017, 1, 1, 5, 0, tzinfo=utc), '2017'), (datetime.datetime(2018, 1, 1, 5, 0, tzinfo=utc), '2018'), (datetime.datetime(2019, 1, 1, 5, 0, tzinfo=utc), '2019'), (datetime.datetime(2020, 1, 1, 5, 0, tzinfo=utc), '2020+')])),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='resume', to='membership.Member')),
            ],
        ),
        migrations.CreateModel(
            name='ResumeShares',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='share_group', to='auth.Group')),
                ('resumes', models.ManyToManyField(related_name='shared_with', to='resumes.Resume')),
            ],
        ),
    ]