# Generated by Django 2.2.5 on 2019-09-18 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feeraterecord',
            name='delete_time',
        ),
        migrations.RemoveField(
            model_name='paymentcompany',
            name='delete_time',
        ),
        migrations.RemoveField(
            model_name='paymentmethod',
            name='delete_time',
        ),
        migrations.AlterField(
            model_name='feeraterecord',
            name='extends',
            field=models.TextField(blank=True, default='', null=True, verbose_name='扩展数据(json格式存储)'),
        ),
        migrations.AlterField(
            model_name='feeraterecord',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
        migrations.AlterField(
            model_name='paymentcompany',
            name='extends',
            field=models.TextField(blank=True, default='', null=True, verbose_name='扩展数据(json格式存储)'),
        ),
        migrations.AlterField(
            model_name='paymentcompany',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='extends',
            field=models.TextField(blank=True, default='', null=True, verbose_name='扩展数据(json格式存储)'),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
    ]