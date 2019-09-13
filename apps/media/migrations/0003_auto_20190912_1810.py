# Generated by Django 2.2.5 on 2019-09-12 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0002_auto_20190912_1753'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlesmedia',
            options={'ordering': ('-sort', '-add_time'), 'verbose_name': '文章媒体', 'verbose_name_plural': '文章媒体'},
        ),
        migrations.AddField(
            model_name='systemmedia',
            name='link',
            field=models.CharField(default='', max_length=200, verbose_name='链接'),
        ),
        migrations.AlterField(
            model_name='productmedia',
            name='position',
            field=models.CharField(choices=[('cover', '封面'), ('slider', '轮播图'), ('detail', '详情')], max_length=10, verbose_name='媒体位置'),
        ),
    ]