# Generated by Django 2.2.5 on 2019-09-12 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('logistics', '0003_auto_20190912_1333'),
        ('product', '0004_availablespec_interactedproduct'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AfterSalesRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.PositiveIntegerField(default=0, verbose_name='排序优先级')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否启用')),
                ('is_delete', models.BooleanField(default=True, verbose_name='是否删除')),
                ('delete_time', models.DateTimeField(blank=True, default=0, null=True, verbose_name='删除时间')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('extends', models.TextField(blank=True, null=True, verbose_name='扩展数据(json格式存储)')),
                ('status', models.CharField(choices=[('confirming', '等待卖家确认'), ('returning', '等待退货'), ('refunding', '等待退款'), ('refunded', '已退款'), ('refused', '卖家拒绝'), ('finished', '已完成售后'), ('cancelled', '买家取消售后请求')], default='', max_length=20, verbose_name='售后状态')),
                ('demand', models.CharField(choices=[('return', '退货退款'), ('refund', '直接退款'), ('part_refund', '部分退款'), ('change', '更换商品')], default='', max_length=20, verbose_name='售后要求')),
                ('reason', models.TextField(default='', verbose_name='售后理由')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='申请售后产品数量')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=18, verbose_name='申请退款金额')),
                ('message', models.TextField(default='', verbose_name='处理备注')),
                ('need_return', models.BooleanField(default=False, verbose_name='是否要求客户退货')),
                ('tracking_no', models.CharField(default='', max_length=100, verbose_name='物流追踪号')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='after_sales_demands', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
                ('express', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='logistics.LogisticsCompany', verbose_name='快递公司')),
            ],
            options={
                'verbose_name': '售后记录',
                'verbose_name_plural': '售后记录',
                'db_table': 't_after_sales_records',
                'ordering': ('-add_time',),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.PositiveIntegerField(default=0, verbose_name='排序优先级')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否启用')),
                ('is_delete', models.BooleanField(default=True, verbose_name='是否删除')),
                ('delete_time', models.DateTimeField(blank=True, default=0, null=True, verbose_name='删除时间')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('extends', models.TextField(blank=True, null=True, verbose_name='扩展数据(json格式存储)')),
                ('order_no', models.CharField(default='', max_length=30, verbose_name='订单号')),
                ('note', models.CharField(default='', max_length=255, verbose_name='订单备注')),
                ('tracking_no', models.CharField(default='', max_length=100, verbose_name='物流追踪号')),
                ('order_status', models.CharField(choices=[('cart', '购物车'), ('confirmed', '已确认'), ('processing', '处理中'), ('shipped', '已发货'), ('finished', '已完结'), ('after_sales', '发生售后'), ('cancelled', '已取消')], default='', max_length=20, verbose_name='订单状态')),
                ('payment_status', models.CharField(choices=[('unpaid', '未支付'), ('paid', '已支付')], default='', max_length=20, verbose_name='支付状态')),
                ('premium', models.DecimalField(decimal_places=2, max_digits=18, verbose_name='溢价')),
                ('promotion', models.DecimalField(decimal_places=2, max_digits=18, verbose_name='优惠')),
                ('use_balance', models.DecimalField(decimal_places=2, max_digits=18, verbose_name='使用余额')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=18, verbose_name='总金额')),
                ('total_quantity', models.IntegerField(default=0, verbose_name='总商品数')),
                ('consignee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='be_consignee_orders', to='logistics.ShippingInfo', verbose_name='收件人信息')),
                ('consignor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='be_consignor_orders', to='logistics.ShippingInfo', verbose_name='发件人信息')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='purchase_orders', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
                ('express', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='logistics.LogisticsCompany', verbose_name='快递公司')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='payment.PaymentMethod', verbose_name='支付方式')),
            ],
            options={
                'verbose_name': '订单',
                'verbose_name_plural': '订单',
                'db_table': 't_orders',
                'ordering': ('-add_time',),
            },
        ),
        migrations.CreateModel(
            name='OrderStatusHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.PositiveIntegerField(default=0, verbose_name='排序优先级')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否启用')),
                ('is_delete', models.BooleanField(default=True, verbose_name='是否删除')),
                ('delete_time', models.DateTimeField(blank=True, default=0, null=True, verbose_name='删除时间')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('extends', models.TextField(blank=True, null=True, verbose_name='扩展数据(json格式存储)')),
                ('previous_status', models.CharField(choices=[('cart', '购物车'), ('confirmed', '已确认'), ('processing', '处理中'), ('shipped', '已发货'), ('finished', '已完结'), ('after_sales', '发生售后'), ('cancelled', '已取消')], default='', max_length=20, verbose_name='前一个状态')),
                ('current_status', models.CharField(choices=[('cart', '购物车'), ('confirmed', '已确认'), ('processing', '处理中'), ('shipped', '已发货'), ('finished', '已完结'), ('after_sales', '发生售后'), ('cancelled', '已取消')], default='', max_length=20, verbose_name='前一个状态')),
                ('message', models.CharField(default='', max_length=200, verbose_name='变更原因')),
                ('note', models.TextField(default='', verbose_name='状态变更备注')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='引起订单状态变更的用户')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='histories', to='order.Order', verbose_name='相关订单')),
            ],
            options={
                'verbose_name': '订单状态变更记录',
                'verbose_name_plural': '订单状态变更记录',
                'db_table': 't_order_status_history',
                'ordering': ('-add_time',),
            },
        ),
        migrations.CreateModel(
            name='OrderRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.PositiveIntegerField(default=0, verbose_name='排序优先级')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否启用')),
                ('is_delete', models.BooleanField(default=True, verbose_name='是否删除')),
                ('delete_time', models.DateTimeField(blank=True, default=0, null=True, verbose_name='删除时间')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('extends', models.TextField(blank=True, null=True, verbose_name='扩展数据(json格式存储)')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=18, verbose_name='价格')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=18, verbose_name='购买数量')),
                ('unit_promotion', models.DecimalField(decimal_places=2, max_digits=18, verbose_name='针对某个产品的优惠')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='order.Order', verbose_name='所属订单')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='orders', to='product.Product', verbose_name='所购商品')),
                ('spec', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='product.Spec', verbose_name='所购型号')),
            ],
            options={
                'verbose_name': '订单记录',
                'verbose_name_plural': '订单记录',
                'db_table': 't_order_Records',
                'ordering': ('-add_time',),
            },
        ),
        migrations.CreateModel(
            name='AfterSalesStatusHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.PositiveIntegerField(default=0, verbose_name='排序优先级')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否启用')),
                ('is_delete', models.BooleanField(default=True, verbose_name='是否删除')),
                ('delete_time', models.DateTimeField(blank=True, default=0, null=True, verbose_name='删除时间')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('extends', models.TextField(blank=True, null=True, verbose_name='扩展数据(json格式存储)')),
                ('previous_status', models.CharField(choices=[('confirming', '等待卖家确认'), ('returning', '等待退货'), ('refunding', '等待退款'), ('refunded', '已退款'), ('refused', '卖家拒绝'), ('finished', '已完成售后'), ('cancelled', '买家取消售后请求')], default='', max_length=20, verbose_name='前一个状态')),
                ('current_status', models.CharField(choices=[('confirming', '等待卖家确认'), ('returning', '等待退货'), ('refunding', '等待退款'), ('refunded', '已退款'), ('refused', '卖家拒绝'), ('finished', '已完成售后'), ('cancelled', '买家取消售后请求')], default='', max_length=20, verbose_name='前一个状态')),
                ('message', models.CharField(default='', max_length=200, verbose_name='变更原因')),
                ('note', models.TextField(default='', verbose_name='状态变更备注')),
                ('after_sales_record', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='histories', to='order.AfterSalesRecord', verbose_name='相关售后')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='引起订单状态变更的用户')),
            ],
            options={
                'verbose_name': '售后记录状态变更历史',
                'verbose_name_plural': '售后记录状态变更历史',
                'db_table': 't_after_sales_status_history',
                'ordering': ('-add_time',),
            },
        ),
        migrations.AddField(
            model_name='aftersalesrecord',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='after_sales_records', to='order.Order', verbose_name='相关订单'),
        ),
        migrations.AddField(
            model_name='aftersalesrecord',
            name='order_record',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='order.OrderRecord', verbose_name='相关订单记录'),
        ),
        migrations.AddField(
            model_name='aftersalesrecord',
            name='shipping_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='logistics.ShippingInfo', verbose_name='退货地址'),
        ),
    ]
