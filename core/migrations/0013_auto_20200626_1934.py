# Generated by Django 3.0.7 on 2020-06-26 22:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20200626_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='current_year',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Year'),
        ),
    ]
