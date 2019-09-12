# Generated by Django 2.2.5 on 2019-09-11 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExpressFeeGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.PositiveIntegerField(default=0, verbose_name='排序优先级')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否启用')),
                ('is_delete', models.BooleanField(default=True, verbose_name='是否删除')),
                ('delete_time', models.DateTimeField(blank=True, default=0, null=True, verbose_name='删除时间')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('extends', models.TextField(blank=True, null=True, verbose_name='扩展数据(json格式存储)')),
            ],
            options={
                'verbose_name': '快递费分组',
                'verbose_name_plural': '快递费分组',
                'db_table': 't_express_fee_groups',
                'ordering': ('-sort', '-add_time'),
            },
        ),
        migrations.CreateModel(
            name='ExpressFeeRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.PositiveIntegerField(default=0, verbose_name='排序优先级')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否启用')),
                ('is_delete', models.BooleanField(default=True, verbose_name='是否删除')),
                ('delete_time', models.DateTimeField(blank=True, default=0, null=True, verbose_name='删除时间')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('extends', models.TextField(blank=True, null=True, verbose_name='扩展数据(json格式存储)')),
            ],
            options={
                'verbose_name': '快递费设置记录',
                'verbose_name_plural': '快递费设置记录',
                'db_table': 't_express_fee_records',
                'ordering': ('-sort', '-add_time'),
            },
        ),
        migrations.CreateModel(
            name='LogisticsCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.PositiveIntegerField(default=0, verbose_name='排序优先级')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否启用')),
                ('is_delete', models.BooleanField(default=True, verbose_name='是否删除')),
                ('delete_time', models.DateTimeField(blank=True, default=0, null=True, verbose_name='删除时间')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('extends', models.TextField(blank=True, null=True, verbose_name='扩展数据(json格式存储)')),
                ('name', models.CharField(default='', max_length=50, verbose_name='公司名')),
                ('website', models.CharField(default='', max_length=200, verbose_name='网站')),
                ('address', models.CharField(default='', max_length=200, verbose_name='地址')),
                ('tracking_no_role', models.CharField(default='', max_length=100, verbose_name='单号验证规则')),
                ('api_url', models.CharField(default='', max_length=200, verbose_name='查询api')),
                ('api_id', models.CharField(default='', max_length=200, verbose_name='查询api登录id')),
                ('api_token', models.CharField(default='', max_length=200, verbose_name='查询api的token')),
                ('api_key', models.CharField(default='', max_length=200, verbose_name='查询api的key')),
                ('api_callback', models.CharField(default='', max_length=200, verbose_name='查询api的回调地址')),
            ],
            options={
                'verbose_name': '快递公司',
                'verbose_name_plural': '快递公司',
                'db_table': 't_logistics_companies',
                'ordering': ('-sort', '-add_time'),
            },
        ),
        migrations.CreateModel(
            name='TrackingNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.PositiveIntegerField(default=0, verbose_name='排序优先级')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否启用')),
                ('is_delete', models.BooleanField(default=True, verbose_name='是否删除')),
                ('delete_time', models.DateTimeField(blank=True, default=0, null=True, verbose_name='删除时间')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('extends', models.TextField(blank=True, null=True, verbose_name='扩展数据(json格式存储)')),
            ],
            options={
                'verbose_name': '快递单号',
                'verbose_name_plural': '快递单号',
                'db_table': 't_tracking_numbers',
                'ordering': ('-sort', '-add_time'),
            },
        ),
    ]
