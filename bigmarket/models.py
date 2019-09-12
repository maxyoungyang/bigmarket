from django.db import models


class BaseModel(models.Model):
    """
    将模型对象的公共字段抽象到一个基类中
    """
    sort = models.PositiveIntegerField(verbose_name='排序优先级', default=0)
    is_enable = models.BooleanField(verbose_name='是否启用', default=True)
    is_delete = models.BooleanField(verbose_name='是否删除', default=True)
    delete_time = models.DateTimeField(verbose_name='删除时间', default=0, blank=True, null=True)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    extends = models.TextField(verbose_name='扩展数据(json格式存储)', blank=True, null=True)

    class Meta:
        """
        在Meta类中设置 abstract = True 则不会在数据库中生成表
        """
        abstract = True
