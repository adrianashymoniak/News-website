# Generated by Django 3.0.5 on 2020-04-10 20:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_auto_20200410_1949'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_on']},
        ),
        migrations.AddField(
            model_name='comment',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2020, 4, 10, 20, 41, 32, 980900, tzinfo=utc)),
            preserve_default=False,
        ),
    ]