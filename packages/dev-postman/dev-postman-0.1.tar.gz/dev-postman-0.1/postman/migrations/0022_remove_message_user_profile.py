# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postman', '0021_auto_20160622_1054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='user_profile',
        ),
    ]
