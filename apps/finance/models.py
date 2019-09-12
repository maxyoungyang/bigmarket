""" 财务管理模块 """
from django.db import models

from apps.user.models import User
from bigmarket.models import BaseModel
from bigmarket.choices import Choices


# 交易记录模型
class TransactionRecord(BaseModel):
    """
    所有电子货币的交易记录模型
    """
    user = models.ForeignKey(User, verbose_name='交易记录所属用户', on_delete=models.CASCADE, related_name='trans_records')
    currency = models.CharField('电子币种', default='', max_length=20, choices=Choices.CURRENCY_TYPE_CHOICES)
    current_amount = models.DecimalField('当前金额', default=0, max_digits=18, decimal_places=2)
    change = models.DecimalField('变化金额', default=0, max_digits=18, decimal_places=2)

    def __str__(self):
        return self.user.mobile + ' - ' + self.currency + ' - ' + self.change

    class Meta:
        verbose_name = '交易记录'
        verbose_name_plural = verbose_name
        db_table = 't_transaction_records'
        ordering = ('-add_time',)
