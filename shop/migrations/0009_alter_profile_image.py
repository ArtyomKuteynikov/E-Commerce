# Generated by Django 4.1.7 on 2023-03-24 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile_pics'),
        ),
    ]
