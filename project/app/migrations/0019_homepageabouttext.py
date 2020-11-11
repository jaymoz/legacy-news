# Generated by Django 3.1.3 on 2020-11-11 09:49

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_footerlinks'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomepageAboutText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', tinymce.models.HTMLField(blank=True, null=True)),
            ],
        ),
    ]
