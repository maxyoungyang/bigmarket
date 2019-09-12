# Generated by Django 2.2.5 on 2019-09-12 11:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0003_inventoryhistory_product_spec_specdetail'),
    ]

    operations = [
        migrations.CreateModel(
            name='InteractedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.PositiveIntegerField(default=0, verbose_name='排序优先级')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否启用')),
                ('is_delete', models.BooleanField(default=True, verbose_name='是否删除')),
                ('delete_time', models.DateTimeField(blank=True, default=0, null=True, verbose_name='删除时间')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('extends', models.TextField(blank=True, null=True, verbose_name='扩展数据(json格式存储)')),
                ('type', models.CharField(choices=[('like', '点赞'), ('fav', '收藏'), ('sale', '销售'), ('watched', '看过')], max_length=20, verbose_name='行为')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='users', to='product.Product', verbose_name='相关商品')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='interacted_products', to=settings.AUTH_USER_MODEL, verbose_name='所属用户')),
            ],
            options={
                'verbose_name': '互动商品记录',
                'verbose_name_plural': '互动商品记录',
                'db_table': 't_interacted_products',
                'ordering': ('-add_time',),
            },
        ),
        migrations.CreateModel(
            name='AvailableSpec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.PositiveIntegerField(default=0, verbose_name='排序优先级')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否启用')),
                ('is_delete', models.BooleanField(default=True, verbose_name='是否删除')),
                ('delete_time', models.DateTimeField(blank=True, default=0, null=True, verbose_name='删除时间')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('extends', models.TextField(blank=True, null=True, verbose_name='扩展数据(json格式存储)')),
                ('spec', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='users', to='product.Spec', verbose_name='相关规格')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='available_specs', to=settings.AUTH_USER_MODEL, verbose_name='所属用户')),
            ],
            options={
                'verbose_name': '可售规格记录',
                'verbose_name_plural': '可售规格记录',
                'db_table': 't_available_specs',
                'ordering': ('-add_time',),
            },
        ),
    ]
