# Generated by Django 2.2.5 on 2019-09-18 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20190914_1357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aftersalesrecord',
            name='delete_time',
        ),
        migrations.RemoveField(
            model_name='aftersalesstatushistory',
            name='delete_time',
        ),
        migrations.RemoveField(
            model_name='order',
            name='delete_time',
        ),
        migrations.RemoveField(
            model_name='orderrecord',
            name='delete_time',
        ),
        migrations.RemoveField(
            model_name='orderstatushistory',
            name='delete_time',
        ),
        migrations.AlterField(
            model_name='aftersalesrecord',
            name='extends',
            field=models.TextField(blank=True, default='', null=True, verbose_name='扩展数据(json格式存储)'),
        ),
        migrations.AlterField(
            model_name='aftersalesrecord',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
        migrations.AlterField(
            model_name='aftersalesstatushistory',
            name='extends',
            field=models.TextField(blank=True, default='', null=True, verbose_name='扩展数据(json格式存储)'),
        ),
        migrations.AlterField(
            model_name='aftersalesstatushistory',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
        migrations.AlterField(
            model_name='order',
            name='extends',
            field=models.TextField(blank=True, default='', null=True, verbose_name='扩展数据(json格式存储)'),
        ),
        migrations.AlterField(
            model_name='order',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
        migrations.AlterField(
            model_name='orderrecord',
            name='extends',
            field=models.TextField(blank=True, default='', null=True, verbose_name='扩展数据(json格式存储)'),
        ),
        migrations.AlterField(
            model_name='orderrecord',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
        migrations.AlterField(
            model_name='orderstatushistory',
            name='extends',
            field=models.TextField(blank=True, default='', null=True, verbose_name='扩展数据(json格式存储)'),
        ),
        migrations.AlterField(
            model_name='orderstatushistory',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
    ]