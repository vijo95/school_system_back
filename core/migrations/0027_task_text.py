# Generated by Django 3.0.7 on 2020-06-27 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20200627_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]