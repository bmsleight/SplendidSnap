# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('appsplendid', '0002_auto_20150720_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='splendid',
            name='free',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='splendid',
            name='pair_image',
            field=models.FileField(null=True, upload_to=b'pdfs', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='splendid',
            name='creator',
            field=models.CharField(help_text=b'Enter your twitter username to get a tweet when the pack has been created and is ready for download', max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='splendid',
            name='image_zip_file',
            field=models.FileField(help_text=b'A zip file containing images to be used on the cards. <br>A pack can consist of just words, just images from the zip file or a mixture of images and words.', null=True, upload_to=b'zips', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='splendid',
            name='images_per_card',
            field=models.IntegerField(help_text=b'Between 3 and 7 images per card', validators=[django.core.validators.MinValueValidator(3), django.core.validators.MaxValueValidator(8)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='splendid',
            name='pack_name',
            field=models.CharField(help_text=b'Name of you pack of cards, e.g. SplendidSigns', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='splendid',
            name='source_of_images',
            field=models.TextField(help_text=b'What are the orginas of your images. For examples where did you download them. <br/>e.g. Traffic signs images downloaded from https://www.gov.uk/traffic-sign-images.<br/>Traffic signs are Crown copyright and used under http://www.nationalarchives.gov.uk/doc/open-government-licence/', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='splendid',
            name='words',
            field=models.TextField(help_text=b"A list of words seperated by a comma. To have more than one line use \\n as a return:<br/>e.g. Merci, S'il vous pla\xc3\xaet, Au revoir, \xc3\x87a va?\\nHow are you? ", null=True, blank=True),
            preserve_default=True,
        ),
    ]
