# Generated by Django 3.0.7 on 2020-06-30 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_test_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='studenttest',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
