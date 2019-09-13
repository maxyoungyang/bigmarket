"""
用户模块 模型定义
"""
from django.db import models
from django.contrib.auth.models import AbstractUser

from bigmarket.choices import Choices
from bigmarket.models import BaseModel


class User(AbstractUser):
    mobile = models.CharField(verbose_name='手机号', max_length=18, default='', null=True, blank=True)
    alipay_openid = models.CharField(verbose_name='支付宝openid', max_length=60, default='', null=True, blank=True)
    weixin_openid = models.CharField(verbose_name='微信openid', max_length=60, default='', null=True, blank=True)
    weixin_web_openid = models.CharField(verbose_name='微信web用户openid', max_length=60, default='', null=True, blank=True)
    baidu_openid = models.CharField(verbose_name='百度openid', max_length=60, default='', null=True, blank=True)
    status = models.CharField(verbose_name='用户状态', default='0', choices=Choices.USER_STATUS_CHOICES, max_length=20)
    token = models.CharField(verbose_name='口令字符串', max_length=254, default='')
    user_level = models.CharField(verbose_name='用户等级', default='normal',
                                  choices=Choices.USER_LEVEL_CHOICES, max_length=20)

    class Meta:
        db_table = 't_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.username:
            return self.username
        else:
            return self.mobile


class UserProfile(BaseModel):
    user = models.OneToOneField(User, verbose_name='所属用户', on_delete=models.CASCADE)
    nickname = models.CharField(verbose_name='昵称', max_length=60, default='', null=True, blank=True)
    gender = models.CharField(verbose_name='性别', default='', max_length=6,
                              choices=Choices.GENDER_CHOICES, null=True, blank=True)
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)

    integral = models.DecimalField(verbose_name='积分', default=0, max_digits=18, decimal_places=2)
    locking_integral = models.DecimalField(verbose_name='锁定积分', default=0, max_digits=18, decimal_places=2)
    balance = models.DecimalField(verbose_name='余额', default=0, max_digits=18, decimal_places=2)
    locking_balance = models.DecimalField(verbose_name='锁定余额', default=0, max_digits=18, decimal_places=2)
    financial_balance = models.DecimalField(verbose_name='理财金额', default=0, max_digits=18, decimal_places=2)
    locking_financial_balance = models.DecimalField(verbose_name='锁定理财金额', default=0, max_digits=18,
                                                    decimal_places=2)

    referrer = models.ForeignKey('self', verbose_name='推荐人', related_name='team',
                                 on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = 't_user_profiles'
        ordering = ('-sort', '-add_time',)
        verbose_name = '个人信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.nickname:
            return self.nickname
        else:
            return self.user.mobile


class AgentGroup(BaseModel):
    supplier = models.ForeignKey(User, verbose_name='供应商', on_delete=models.DO_NOTHING)
    name = models.CharField(verbose_name='代理分组名称', max_length=50, default='', null=True, blank=True)
    desc = models.CharField(verbose_name='代理分组描述', max_length=200, default='', null=True, blank=True)

    def __str__(self):
        return self.supplier.mobile + ' - ' + self.name

    class Meta:
        db_table = 't_agent_groups'
        ordering = ('-sort', '-add_time',)
        verbose_name = '代理分组'
        verbose_name_plural = verbose_name


class Agent(BaseModel):
    agent_group = models.ForeignKey(AgentGroup, verbose_name='所属分组', on_delete=models.DO_NOTHING)
    supplier = models.ForeignKey(User, verbose_name='供应商', on_delete=models.DO_NOTHING, related_name='suppliers')
    agent = models.ForeignKey(User, verbose_name='代理', on_delete=models.DO_NOTHING, related_name='agents')

    def __str__(self):
        return self.agent.mobile

    class Meta:
        db_table = 't_agents'
        ordering = ('-sort', '-add_time',)
        verbose_name = '代理'
        verbose_name_plural = verbose_name


# 用户登录记录
class LoginRecord(BaseModel):
    """
    用户登录记录
    与users表是多对一的关系
    login_time记录用户本次登录时间
    login_ip记录用户本次登录ip地址
    """
    user = models.ForeignKey(User, verbose_name='登录用户', on_delete=models.CASCADE,
                             related_name='login_records')
    login_ip = models.GenericIPAddressField(verbose_name='用户此次登录的IP地址', default='')

    class Meta:
        verbose_name = '用户登录记录'
        verbose_name_plural = verbose_name
        db_table = 't_login_records'
        ordering = ('-add_time',)


# 登录验证码
class VerifyCode(BaseModel):
    """
    短信验证码
    """
    code = models.CharField(verbose_name='验证码', max_length=10)
    mobile = models.CharField(verbose_name='手机号', max_length=18, default='', null=True, blank=True)

    class Meta:
        verbose_name = '短信验证码'
        verbose_name_plural = verbose_name
        db_table = 't_verify_codes'
        ordering = ('-add_time',)
