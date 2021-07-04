# Generated by Django 3.2 on 2021-07-04 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0002_auto_20210704_0938'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result',
            old_name='correct_answers',
            new_name='percentage',
        ),
        migrations.AlterField(
            model_name='result',
            name='progress',
            field=models.CharField(choices=[('C', 'Completed'), ('O', 'On_Progress')], max_length=1),
        ),
    ]
