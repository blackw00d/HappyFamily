# Generated by Django 3.0.8 on 2020-11-09 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HFhtml', '0002_orders_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='cityprice',
            name='reserved',
            field=models.IntegerField(default=0, verbose_name='Зарезервировано'),
        ),
    ]
