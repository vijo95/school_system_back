# Generated by Django 3.0.7 on 2020-07-02 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_auto_20200702_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studenttask',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Student'),
        ),
        migrations.AlterField(
            model_name='studenttask',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Task'),
        ),
        migrations.AlterField(
            model_name='studenttest',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Student'),
        ),
    ]
