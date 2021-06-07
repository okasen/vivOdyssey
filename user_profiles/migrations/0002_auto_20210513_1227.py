# Generated by Django 3.1.7 on 2021-05-13 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vivPets', '0008_auto_20210513_1227'),
        ('user_profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='bio',
            field=models.CharField(blank=True, default='Nothing to see here!', max_length=500),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='starredPet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='vivPets.pet'),
        ),
    ]