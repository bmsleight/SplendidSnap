# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Splendid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pack_name', models.CharField(max_length=200)),
                ('creator', models.CharField(max_length=20)),
                ('images_per_card', models.IntegerField(validators=[django.core.validators.MinValueValidator(3), django.core.validators.MaxValueValidator(8)])),
                ('words', models.TextField(null=True)),
                ('image_zip_file', models.FileField(null=True, upload_to=b'zips')),
                ('source_of_images', models.TextField()),
                ('pdf', models.FileField(null=True, upload_to=b'pdfs')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
