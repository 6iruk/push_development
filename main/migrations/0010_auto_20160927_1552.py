# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-09-27 12:52
from __future__ import unicode_literals

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_announcement_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='announcement',
            old_name='file',
            new_name='file1',
        ),
        migrations.AddField(
            model_name='announcement',
            name='file2',
            field=models.FileField(blank=True, upload_to=main.models.upload_path),
        ),
    ]