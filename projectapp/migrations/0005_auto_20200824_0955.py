# Generated by Django 3.1 on 2020-08-24 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectapp', '0004_menulist_resinfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resinfo',
            name='res_long_info',
        ),
        migrations.RemoveField(
            model_name='resinfo',
            name='res_short_info',
        ),
        migrations.AddField(
            model_name='resinfo',
            name='res_info',
            field=models.TextField(null=True, verbose_name='식당 소개'),
        ),
        migrations.AlterField(
            model_name='resinfo',
            name='res_image',
            field=models.CharField(max_length=40, null=True, verbose_name='이미지 경로'),
        ),
        migrations.AlterField(
            model_name='resinfo',
            name='rev_cnt',
            field=models.IntegerField(default=0, verbose_name='총 리뷰수'),
        ),
        migrations.AlterField(
            model_name='resinfo',
            name='star_avg',
            field=models.FloatField(default=0, verbose_name='리뷰 별점의 평균 = 총 별점'),
        ),
    ]