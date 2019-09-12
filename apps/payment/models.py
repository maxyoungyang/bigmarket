""" 支付方模块 """
from django.db import models

from bigmarket.choices import Choices
from bigmarket.models import BaseModel


# 支付方式
class PaymentMethod(BaseModel):
    """
    支付方式模型
    """
    name = models.CharField(verbose_name='名称', default='', max_length=50)
    use_for = models.CharField(verbose_name='适用终端', default='', max_length=1, choices=Choices.USE_FOR_CHOICES)
    currency = models.CharField(verbose_name='结算币种', default='', max_length=3)
    account = models.CharField(verbose_name='商户号', default='', max_length=30)
    appid = models.CharField(verbose_name='appid', default='', max_length=30)
    key = models.CharField(verbose_name='签名密钥', default='', max_length=30)
    callback_url_1 = models.CharField(verbose_name='签名密钥1', default='', max_length=200)
    callback_url_2 = models.CharField(verbose_name='签名密钥2', default='', max_length=200)
    callback_url_3 = models.CharField(verbose_name='签名密钥3', default='', max_length=200)
    is_usable = models.BooleanField(verbose_name='是否对用户开放', default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 't_payment_methods'
        ordering = ('-sort', '-add_time')


# 三方支付公司
class PaymentCompany(BaseModel):
    """
    三方支付公司模型
    """
    name = models.CharField(verbose_name='公司名', default='', max_length=50)
    spell = models.CharField(verbose_name='拼写', default='', max_length=50)
    website = models.CharField(verbose_name='网站', default='', max_length=200, null=True, blank=True)
    address = models.CharField(verbose_name='地址', default='', max_length=200, null=True, blank=True)
    contact = models.CharField(verbose_name='联系人', default='', max_length=10, null=True, blank=True)
    mobile = models.CharField(verbose_name='联系人电话', default='', max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '支付公司'
        verbose_name_plural = verbose_name
        ordering = ('-sort', '-add_time',)
        db_table = 't_payment_companies'


# 支付费率
class FeeRateRecord(BaseModel):
    company = models.ForeignKey(PaymentCompany, verbose_name='支付公司',
                                on_delete=models.CASCADE, related_name='fee_rate_records')
    payment_method = models.CharField(verbose_name='支付方式', max_length=20, choices=Choices.PAYMENT_METHOD_CHOICES)
    rate = models.DecimalField(verbose_name='费率', max_digits=10, decimal_places=5)

    def __str__(self):
        return self.company.name + '--' + self.payment_method + '--' + str(self.rate)

    class Meta:
        verbose_name = '支付费率'
        verbose_name_plural = verbose_name
        ordering = ('-sort', '-add_time',)
        db_table = 't_fee_rate_records'

