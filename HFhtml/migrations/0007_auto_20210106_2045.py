# Generated by Django 3.0.8 on 2021-01-06 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HFhtml', '0006_auto_20210106_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='pay',
            field=models.TextField(choices=[('Онлайн', 'Онлайн'), ('При получении', 'При получении')], default='Онлайн', verbose_name='Оплата'),
        ),
    ]
