# Generated by Django 3.2.9 on 2021-12-01 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0007_auto_20211130_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='gradedassignment',
            name='score',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gradedassignment',
            name='wrong_answer',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]