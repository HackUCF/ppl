from datetime import datetime

from django.contrib.auth.models import Group
from django.db import models
from dateutil.tz import gettz

from membership.models import Member

eastern_tz = gettz('America/New_York')


class ResumeShares(models.Model):
    group = models.OneToOneField(Group, related_name='share_group')
    resumes = models.ManyToManyField('Resume', related_name='shared_with')


class Resume(models.Model):
    GRADUATION_CHOICES = (
        (datetime(2015, 12, 18, tzinfo=eastern_tz), 'Fall 2015'),
        (datetime(2015, 5, 5, tzinfo=eastern_tz), 'Spring 2016'),
        (datetime(2015, 8, 6, tzinfo=eastern_tz), 'Summer 2016'),
        (datetime(2016, 12, 18, tzinfo=eastern_tz), 'Fall 2016'),
        (datetime(2017, 1, 1, tzinfo=eastern_tz), '2017'),
        (datetime(2018, 1, 1, tzinfo=eastern_tz), '2018'),
        (datetime(2019, 1, 1, tzinfo=eastern_tz), '2019'),
        (datetime(2020, 1, 1, tzinfo=eastern_tz), '2020+'),
    )
    GRADUATION_DATES = {name: dt for dt, name in GRADUATION_CHOICES}

    timestamp = models.DateTimeField()
    member = models.OneToOneField(to=Member, related_name='resume')
    url = models.URLField(unique=True)
    graduation = models.DateTimeField(choices=GRADUATION_CHOICES)
