# Generated by Django 3.1.4 on 2021-01-09 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='date_answered',
            field=models.DateField(),
        ),
    ]
