# Generated by Django 3.2.4 on 2021-06-30 05:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('viv_pets', '0014_auto_20210630_0655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2021, 6, 30, 5, 55, 48, 605767, tzinfo=utc)),
        ),
    ]