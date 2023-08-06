# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hcore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='maintainers',
            field=models.ManyToManyField(related_name='maintaining_stations', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
