# Generated by Django 3.0.2 on 2020-01-11 08:23

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('games', '0002_auto_20200111_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
