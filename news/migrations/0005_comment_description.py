# Generated by Django 3.0.5 on 2020-04-10 12:55

from django.db import migrations
import froala_editor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20200408_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='description',
            field=froala_editor.fields.FroalaField(null=True),
        ),
    ]
