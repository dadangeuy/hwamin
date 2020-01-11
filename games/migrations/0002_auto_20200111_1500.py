# Generated by Django 3.0.2 on 2020-01-11 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('source_id', models.CharField(editable=False, max_length=33)),
                ('point', models.IntegerField(default=0)),
                ('profile', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
            ],
        ),
        migrations.AddConstraint(
            model_name='score',
            constraint=models.UniqueConstraint(fields=('source_id', 'profile'), name='score_has_unique_source_id_and_profile'),
        ),
    ]