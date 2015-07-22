# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appsplendid', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='splendid',
            name='image_zip_file',
            field=models.FileField(null=True, upload_to=b'zips', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='splendid',
            name='pdf',
            field=models.FileField(null=True, upload_to=b'pdfs', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='splendid',
            name='source_of_images',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
