from django.db import models

from apps.user.models import AgentGroup
from bigmarket.models import BaseModel


class Promotion(BaseModel):
    agent_group = models.ForeignKey(AgentGroup, verbose_name='所属代理分组', on_delete=models.DO_NOTHING)
    amount = models.DecimalField(verbose_name='建议零售价', max_digits=18, decimal_places=2)

    class Meta:
        verbose_name = '优惠'
        verbose_name_plural = verbose_name
        db_table = 't_promotions'
        ordering = ('-sort', '-add_time',)
