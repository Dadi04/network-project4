# Generated by Django 4.2.3 on 2023-08-31 11:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_alter_newpost_timestamp_alter_likes_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newpost',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 31, 11, 1, 37, 92901, tzinfo=datetime.timezone.utc)),
        ),
    ]