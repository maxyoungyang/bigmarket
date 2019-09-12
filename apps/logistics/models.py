""" 快递模块 """
from django.db import models

from apps.user.models import User
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


# 物流信息 TODO
class TrackingRecord(BaseModel):
    class Meta:
        verbose_name = '追踪信息记录'
        verbose_name_plural = verbose_name
        ordering = ('-sort', '-add_time',)
        db_table = 't_tracking_records'


# 地区模型
class Region(BaseModel):
    """
    地区模型
    分四级，省市县街道
    如果没有父级地区，则parent_id = 0
    先按等级再按名称排序
    """
    parent = models.ForeignKey('self', verbose_name='父级地区',
                               on_delete=models.CASCADE, db_column='parent_id', related_name='jurisdictions')
    name = models.CharField(verbose_name='地区名称', max_length=255, default='')
    level = models.PositiveIntegerField(verbose_name='级别类型 1:国家, 2:省, 3:市, 4:区县, 5:街道, 9:其他')
    spell = models.CharField(verbose_name='拼写', max_length=60, default='')

    class Meta:
        verbose_name = '地区'
        verbose_name_plural = verbose_name
        ordering = ('-sort', '-add_time',)
        db_table = 't_regions'


# 物流信息
class ShippingInfo(BaseModel):
    """
    收/发件人邮政信息模型
    """
    user = models.ForeignKey(User, verbose_name='创建该邮寄信息的用户',
                             on_delete=models.CASCADE, related_name='shipping_info_book', null=True, blank=True)

    id_number = models.CharField(verbose_name='收件人身份证号', max_length=20, default='', null=True, blank=True)
    id_photo_front = models.ImageField(verbose_name='收件人身份证正面照片', default='',
                                       upload_to='media/image/id', null=True, blank=True)
    id_photo_back = models.ImageField(verbose_name='收件人身份证背面照片', default='',
                                      upload_to='media/image/id', null=True, blank=True)

    alias = models.CharField(verbose_name='别名', max_length=60, default='', null=True, blank=True)

    name = models.CharField(verbose_name='收件人姓名', max_length=60, default='')
    telephone = models.CharField(verbose_name='收件人联系电话', max_length=20, default='')

    country = models.PositiveIntegerField(verbose_name='收件人地址-国家', default=1, null=True, blank=True)
    province = models.PositiveIntegerField(verbose_name='收件人地址-省', default=1)
    city = models.PositiveIntegerField(verbose_name='收件人地址-市', default=1)
    district = models.PositiveIntegerField(verbose_name='收件人地址-区县', default=1)
    street = models.PositiveIntegerField(verbose_name='收件人地址-街道 乡村', default=1, null=True, blank=True)
    detail = models.CharField(verbose_name='收件人地址-具体地址', max_length=254, default='')
    postcode = models.CharField(verbose_name='邮编', max_length=20, default='', null=True, blank=True)

    is_default = models.BooleanField(verbose_name='是否为默认收件人地址', default=False)
    is_sender = models.BooleanField(verbose_name='是否为发件人地址', default=False)
    last_use_time = models.DateTimeField(verbose_name='用户最后使用这个邮寄信息的时间', null=True, blank=True)

    def __str__(self):
        return self.name + ' - ' + self.telephone

    class Meta:
        verbose_name = '地址信息'
        verbose_name_plural = verbose_name
        ordering = ('-sort', '-add_time',)
        db_table = 't_shipping_infos'

