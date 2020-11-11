# Generated by Django 3.1.3 on 2020-11-11 11:13

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_footerlinks_footer_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepageabouttext',
            name='website_name_on_homepage',
            field=tinymce.models.HTMLField(blank=True, max_length=150, null=True),
        ),
    ]
