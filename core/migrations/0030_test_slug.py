# Generated by Django 3.0.7 on 2020-06-30 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20200629_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
