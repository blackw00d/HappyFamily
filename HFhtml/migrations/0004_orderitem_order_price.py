# Generated by Django 3.0.8 on 2020-11-09 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HFhtml', '0003_cityprice_reserved'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='order_price',
            field=models.FloatField(default=0, verbose_name='Цена'),
        ),
    ]
