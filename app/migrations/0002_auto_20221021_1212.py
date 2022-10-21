# Generated by Django 3.2.15 on 2022-10-21 01:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='additional_resource',
        ),
        migrations.AlterField(
            model_name='session',
            name='questions',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.question'),
        ),
    ]
