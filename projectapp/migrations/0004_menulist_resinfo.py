# Generated by Django 3.1 on 2020-08-24 00:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectapp', '0003_auto_20200820_0958'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('res_name', models.CharField(max_length=30, verbose_name='식당 이름')),
                ('res_type', models.CharField(max_length=4, verbose_name='식당 종류')),
                ('res_addr', models.TextField(verbose_name='식당 주소')),
                ('res_short_info', models.TextField(verbose_name='간단 소개')),
                ('res_long_info', models.TextField(verbose_name='상세 소개')),
                ('res_price', models.IntegerField(verbose_name='가격대')),
                ('res_image', models.CharField(max_length=40, verbose_name='이미지 경로')),
                ('locate_x', models.FloatField(verbose_name='식당 x좌표')),
                ('locate_y', models.FloatField(verbose_name='식당 y좌표')),
                ('tag_tout', models.IntegerField(verbose_name='1:TakeOut, 0:불가')),
                ('tag_solo', models.IntegerField(verbose_name='1:혼밥추천, 0:불가')),
                ('tag_special', models.IntegerField(verbose_name='1:점심특선, 0:없음')),
                ('tag_free', models.IntegerField(verbose_name='1:자율배식, 0:불가')),
                ('star_avg', models.FloatField(verbose_name='리뷰 별점의 평균 = 총 별점')),
                ('rev_cnt', models.IntegerField(verbose_name='총 리뷰수')),
            ],
        ),
        migrations.CreateModel(
            name='Menulist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_name', models.CharField(max_length=30, verbose_name='메뉴 이름')),
                ('menu_price', models.IntegerField(verbose_name='가격')),
                ('res_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectapp.resinfo')),
            ],
        ),
    ]
