# Generated by Django 2.2.14 on 2020-07-25 23:56

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20200724_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teaminfo',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
    ]
