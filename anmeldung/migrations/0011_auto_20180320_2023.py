# Generated by Django 2.0.3 on 2018-03-20 20:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anmeldung', '0010_player_surname2'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='postcode',
            field=models.PositiveIntegerField(default=1000, validators=[django.core.validators.MinValueValidator(99), django.core.validators.MaxValueValidator(1000000)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='club',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
