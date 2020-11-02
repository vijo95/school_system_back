# Generated by Django 3.0.7 on 2020-07-01 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_remove_studenttest_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='slug',
        ),
        migrations.AddField(
            model_name='test',
            name='title',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]