# Generated by Django 4.1.7 on 2023-03-24 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.CharField(db_index=True, default='example@example.com', max_length=200),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(db_index=True, default='+79000000000', max_length=200),
        ),
    ]