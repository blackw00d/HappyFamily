# Generated by Django 3.0.8 on 2020-08-22 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HFhtml', '0012_auto_20200821_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='phone',
            field=models.TextField(default=None, max_length=10, verbose_name='Телефон'),
        ),
    ]
