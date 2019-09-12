""" 快递模块 """
from django.db import models

from bigmarket.models import BaseModel


# 快递公司
class LogisticsCompany(BaseModel):
    """
    快递公司模型
    可以通过tracking_no_role定义该公司快递单号格式验证的正则规则
    根据sort等级排序，等级相同时，按创建时间
    """
    name = models.CharField(verbose_name='公司名', default='', max_length=50)
    website = models.CharField(verbose_name='网站', default='', max_length=200)
    address = models.CharField(verbose_name='地址', default='', max_length=200)
    tracking_no_role = models.CharField(verbose_name='单号验证规则', default='', max_length=100)
    api_url = models.CharField(verbose_name='查询api', default='', max_length=200)
    api_id = models.CharField(verbose_name='查询api登录id', default='', max_length=200)
    api_token = models.CharField(verbose_name='查询api的token', default='', max_length=200)
    api_key = models.CharField(verbose_name='查询api的key', default='', max_length=200)
    api_callback = models.CharField(verbose_name='查询api的回调地址', default='', max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '快递公司'
        verbose_name_plural = verbose_name
        ordering = ('-sort', '-add_time',)
        db_table = 't_logistics_companies'


# 快递费设置分组 TODO
class ExpressFeeGroup(BaseModel):
    class Meta:
        verbose_name = '快递费分组'
        verbose_name_plural = verbose_name
        ordering = ('-sort', '-add_time',)
        db_table = 't_express_fee_groups'


# 快递费设置记录 TODO
class ExpressFeeRecord(BaseModel):
    class Meta:
        verbose_name = '快递费设置记录'
        verbose_name_plural = verbose_name
        ordering = ('-sort', '-add_time',)
        db_table = 't_express_fee_records'


# 快递单号 TODO
class TrackingNumber(BaseModel):
    class Meta:
        verbose_name = '快递单号'
        verbose_name_plural = verbose_name
        ordering = ('-sort', '-add_time',)
        db_table = 't_tracking_numbers'
