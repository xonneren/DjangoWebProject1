# Generated by Django 2.2.28 on 2023-12-06 09:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_auto_20231206_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 12, 6, 12, 54, 58, 617155), verbose_name='Опубликовано'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 12, 6, 12, 54, 58, 618154), verbose_name='Дата комментария'),
        ),
        migrations.AlterField(
            model_name='priem',
            name='date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 12, 6, 12, 54, 58, 620153), verbose_name='Дата приёма'),
        ),
    ]
