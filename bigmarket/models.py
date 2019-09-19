from django.db import models
from .choices import Choices


class BaseModel(models.Model):
    """
    将模型对象的公共字段抽象到一个基类中
    """
    sort = models.PositiveIntegerField(verbose_name='排序优先级', default=0)
    is_enable = models.BooleanField(verbose_name='是否启用', default=True)
    is_delete = models.BooleanField(verbose_name='是否删除', default=False)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    extends = models.TextField(verbose_name='扩展数据(json格式存储)', blank=True, null=True, default='')

    class Meta:
        """
        在Meta类中设置 abstract = True 则不会在数据库中生成表
        """
        abstract = True


class BaseMedia(BaseModel):
    title = models.CharField(verbose_name='标题', max_length=100)
    brief = models.CharField(verbose_name='简述', blank=True, null=True, max_length=255)
    filename = models.CharField(verbose_name='文件名', max_length=200)
    type = models.CharField(verbose_name='媒体类型', max_length=10, choices=Choices.MEDIA_TYPE_CHOICES)

    class Meta:
        """
        在Meta类中设置 abstract = True 则不会在数据库中生成表
        """
        abstract = True