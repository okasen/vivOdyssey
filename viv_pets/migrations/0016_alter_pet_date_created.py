# Generated by Django 3.2.4 on 2021-06-30 06:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('viv_pets', '0015_alter_pet_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2021, 6, 30, 6, 0, 22, 259493, tzinfo=utc)),
        ),
    ]