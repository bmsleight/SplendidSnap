# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('appsplendid', '0003_auto_20150721_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='splendid',
            name='images_per_card',
            field=models.IntegerField(help_text=b'Between 3 and 8 images per card', validators=[django.core.validators.MinValueValidator(3), django.core.validators.MaxValueValidator(8)]),
            preserve_default=True,
        ),
    ]
