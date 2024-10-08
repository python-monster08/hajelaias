# Generated by Django 5.1 on 2024-10-08 08:51

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question_bank', '0021_alter_inputsuggestion_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inputsuggestion',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='questionbank',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='quoteidiomphrase',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
