# Generated by Django 2.2.5 on 2019-09-18 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0004_auto_20190918_0251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pricing',
            name='delete_time',
        ),
        migrations.RemoveField(
            model_name='stepprice',
            name='delete_time',
        ),
        migrations.RemoveField(
            model_name='tieredpricing',
            name='delete_time',
        ),
        migrations.AlterField(
            model_name='pricing',
            name='extends',
            field=models.TextField(blank=True, default='', null=True, verbose_name='扩展数据(json格式存储)'),
        ),
        migrations.AlterField(
            model_name='pricing',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
        migrations.AlterField(
            model_name='stepprice',
            name='extends',
            field=models.TextField(blank=True, default='', null=True, verbose_name='扩展数据(json格式存储)'),
        ),
        migrations.AlterField(
            model_name='stepprice',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
        migrations.AlterField(
            model_name='tieredpricing',
            name='extends',
            field=models.TextField(blank=True, default='', null=True, verbose_name='扩展数据(json格式存储)'),
        ),
        migrations.AlterField(
            model_name='tieredpricing',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
    ]