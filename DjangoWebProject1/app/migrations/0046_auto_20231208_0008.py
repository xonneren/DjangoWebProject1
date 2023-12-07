# Generated by Django 2.2.28 on 2023-12-07 21:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0045_auto_20231207_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 12, 8, 0, 8, 55, 640570), verbose_name='Опубликовано'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 12, 8, 0, 8, 55, 641569), verbose_name='Дата комментария'),
        ),
        migrations.AlterField(
            model_name='priem',
            name='date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 12, 8, 0, 8, 55, 645571), verbose_name='Дата приёма'),
        ),
        migrations.AlterModelTable(
            name='priem',
            table='Priem',
        ),
    ]
