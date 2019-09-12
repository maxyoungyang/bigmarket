# Generated by Django 2.2.5 on 2019-09-11 23:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentCompany',
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
                ('spell', models.CharField(default='', max_length=50, verbose_name='拼写')),
                ('website', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='网站')),
                ('address', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='地址')),
                ('contact', models.CharField(blank=True, default='', max_length=10, null=True, verbose_name='联系人')),
                ('mobile', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='联系人电话')),
            ],
            options={
                'verbose_name': '支付公司',
                'verbose_name_plural': '支付公司',
                'db_table': 't_payment_companies',
                'ordering': ('-sort', '-add_time'),
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.PositiveIntegerField(default=0, verbose_name='排序优先级')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否启用')),
                ('is_delete', models.BooleanField(default=True, verbose_name='是否删除')),
                ('delete_time', models.DateTimeField(blank=True, default=0, null=True, verbose_name='删除时间')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('extends', models.TextField(blank=True, null=True, verbose_name='扩展数据(json格式存储)')),
                ('name', models.CharField(default='', max_length=50, verbose_name='名称')),
                ('use_for', models.CharField(choices=[('web', 'web网站'), ('h5', 'H5'), ('ios', 'IOS'), ('android', 'ANDROID'), ('wechat_mp', '微信小程序'), ('alipay_mp', '支付宝小程序'), ('baidu_mp', '百度小程序')], default='', max_length=1, verbose_name='适用终端')),
                ('currency', models.CharField(default='', max_length=3, verbose_name='结算币种')),
                ('account', models.CharField(default='', max_length=30, verbose_name='商户号')),
                ('appid', models.CharField(default='', max_length=30, verbose_name='appid')),
                ('key', models.CharField(default='', max_length=30, verbose_name='签名密钥')),
                ('callback_url_1', models.CharField(default='', max_length=200, verbose_name='签名密钥1')),
                ('callback_url_2', models.CharField(default='', max_length=200, verbose_name='签名密钥2')),
                ('callback_url_3', models.CharField(default='', max_length=200, verbose_name='签名密钥3')),
                ('is_usable', models.BooleanField(default=False, verbose_name='是否对用户开放')),
            ],
            options={
                'db_table': 't_payment_methods',
                'ordering': ('-sort', '-add_time'),
            },
        ),
        migrations.CreateModel(
            name='FeeRateRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.PositiveIntegerField(default=0, verbose_name='排序优先级')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否启用')),
                ('is_delete', models.BooleanField(default=True, verbose_name='是否删除')),
                ('delete_time', models.DateTimeField(blank=True, default=0, null=True, verbose_name='删除时间')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('extends', models.TextField(blank=True, null=True, verbose_name='扩展数据(json格式存储)')),
                ('payment_method', models.CharField(choices=[('balance', '余额支付'), ('wechat', '微信支付'), ('alipay', '支付宝'), ('debit_card', '银行卡'), ('credit_card', '信用卡'), ('applepay', 'applypay'), ('paypal', 'paypal')], max_length=20, verbose_name='支付方式')),
                ('rate', models.DecimalField(decimal_places=5, max_digits=10, verbose_name='费率')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fee_rate_records', to='payment.PaymentCompany', verbose_name='支付公司')),
            ],
            options={
                'verbose_name': '支付费率',
                'verbose_name_plural': '支付费率',
                'db_table': 't_fee_rate_records',
                'ordering': ('-sort', '-add_time'),
            },
        ),
    ]
