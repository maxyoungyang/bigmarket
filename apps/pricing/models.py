""" 定价模块 """
from django.db import models

from apps.logistics.models import ExpressFeeGroup
from apps.product.models import Spec
from apps.user.models import AgentGroup
from bigmarket.models import BaseModel


class Pricing(BaseModel):
    """
    价格模型
    先按照指定优先级降序排列
    再按照创建时间降序排列
    """
    spec = models.ForeignKey(Spec, verbose_name='所属规格',
                             on_delete=models.DO_NOTHING, related_name='pricing')
    currency = models.CharField(verbose_name='结算币种', default='', max_length=3)
    cost = models.DecimalField(verbose_name='成本价', max_digits=18, decimal_places=2)

    wholesale_price = models.DecimalField(verbose_name='供货价', max_digits=18, decimal_places=2)
    has_tiered_pricing = models.BooleanField(verbose_name='是否设置阶梯价格', default=False)

    retail_price = models.DecimalField(verbose_name='零售价', max_digits=18, decimal_places=2)
    suggested_retail_price = models.DecimalField(verbose_name='建议零售价', max_digits=18, decimal_places=2)

    is_general = models.BooleanField(verbose_name='是否为通用价格', default=True)

    agent_group = models.ForeignKey(AgentGroup, verbose_name='所属分组',
                                    on_delete=models.DO_NOTHING, related_name='pricing_set')

    is_free_shipping = models.BooleanField(verbose_name='是否包邮', default=True)

    express_fee_group = models.ForeignKey(ExpressFeeGroup, verbose_name='快递费模板',
                                          on_delete=models.DO_NOTHING, null=True, blank=True, related_name='pricing')

    class Meta:
        verbose_name = '定价'
        verbose_name_plural = verbose_name
        db_table = 't_pricing'
        ordering = ('-sort', '-add_time',)


class TieredPricing(BaseModel):
    """
    阶梯价格模型
    """
    pricing = models.ForeignKey(Pricing, verbose_name='隶属价格体系',
                              related_name='tiered_pricing', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = '阶梯定价'
        verbose_name_plural = verbose_name
        db_table = 't_tiered_pricing'
        ordering = ('-sort', '-add_time',)


class StepPrice(BaseModel):
    """
    阶梯价格中的分级价格模型
    """
    tiered_pricing = models.ForeignKey(TieredPricing, verbose_name='所属阶梯价格',
                                       on_delete=models.CASCADE, related_name='step_price')
    min_quantity = models.PositiveIntegerField(verbose_name='最小可购买数量', default=0)
    max_quantity = models.PositiveIntegerField(verbose_name='最大可购买数量', default=0)
    price = models.DecimalField(verbose_name='价格', max_digits=18, decimal_places=2)

    class Meta:
        verbose_name = '阶梯价格'
        verbose_name_plural = verbose_name
        db_table = 't_step_prices'
        ordering = ('-sort', '-add_time',)
