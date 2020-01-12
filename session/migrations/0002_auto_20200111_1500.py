# Generated by Django 3.0.2 on 2020-01-11 08:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('session', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('source_id', models.CharField(editable=False, max_length=33)),
                ('point', models.IntegerField(default=0)),
                ('profile', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='account.Profile')),
            ],
        ),
        migrations.AddConstraint(
            model_name='score',
            constraint=models.UniqueConstraint(fields=('source_id', 'profile'), name='score_has_unique_source_id_and_profile'),
        ),
    ]