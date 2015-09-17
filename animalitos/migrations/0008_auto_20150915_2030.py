# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('animalitos', '0007_auto_20150911_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adoptante',
            name='cedula',
            field=models.CharField(max_length=70, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='adoptante',
            name='telefono',
            field=models.CharField(max_length=70, null=True, blank=True),
        ),
    ]
