# Generated by Django 3.1.4 on 2021-01-09 17:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20210108_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='date_of_birth',
            field=models.DateField(default=datetime.date.today, verbose_name='Date'),
        ),
    ]
