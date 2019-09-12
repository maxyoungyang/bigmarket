from django.db import models
from django.contrib.auth.models import AbstractUser

from bigmarket.choices import Choices
from bigmarket.models import BaseModel


class User(AbstractUser):
    mobile = models.CharField(verbose_name='手机号', max_length=11, default='', null=True, blank=True)
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

    # interacted_products = models.ManyToManyField(Product, verbose_name='互动过的商品', related_name='interacted_users',
    #                                              through='InteractiveProduct', through_fields=('profile', 'product'))
    # available_specs = models.ManyToManyField(Spec, verbose_name='销售产品的可售规格',
    #                                          related_name='interacted_users', through='AvailableSpec',
    #                                          through_fields=('profile', 'spec'))

    # role = models.ForeignKey(Role, verbose_name='用户所属的角色组', related_name='members', default=0,
    #     #                          on_delete=models.SET_DEFAULT)
    #     # permissions = models.ManyToManyField(Permission, verbose_name='该用户的特许权限', related_name='users')

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
