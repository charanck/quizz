# Generated by Django 3.2 on 2021-07-04 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0004_alter_result_time_taken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='percentage',
            field=models.FloatField(default=0.0),
        ),
    ]