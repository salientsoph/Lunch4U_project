# Generated by Django 3.1 on 2020-08-19 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test_table',
            name='tres_image',
            field=models.CharField(max_length=40, verbose_name='이미지 경로'),
        ),
        migrations.AlterField(
            model_name='test_table',
            name='tres_name',
            field=models.CharField(max_length=30, verbose_name='식당 이름'),
        ),
    ]