from django.db import models

from apps.user.models import User
from bigmarket.models import BaseModel


# 品牌
class Brand(BaseModel):
    """
    品牌模型
    按给定优先级'sort'排序
    """
    creator = models.ForeignKey(User, verbose_name='创建人', on_delete=models.CASCADE
                                , blank=True, null=True, related_name='created_brands')
    name = models.CharField(verbose_name='名称', max_length=30)
    letter = models.CharField(verbose_name='名称拼写', max_length=30, blank=True, null=True)
    desc = models.TextField(verbose_name='描述', blank=True, null=True)
    slogan = models.CharField(verbose_name='标语', blank=True, null=True, max_length=80)
    bg_color = models.CharField(verbose_name='背景色', blank=True, null=True, max_length=30)
    is_recommended = models.BooleanField(verbose_name='是否首页推荐', default=False)

    class Meta:
        verbose_name = '品牌'
        verbose_name_plural = verbose_name
        ordering = ('-sort', '-add_time',)
        db_table = 't_brands'

    def __str__(self):
        return self.name


# 商品分类
class Category(BaseModel):
    parent = models.ForeignKey('self', verbose_name='父级分类',
                               on_delete=models.DO_NOTHING, db_column='pid', blank=True, null=True)
    name = models.CharField(verbose_name='分类名称', max_length=30, default='')
    vice_name = models.CharField(verbose_name='分类副标题', blank=True, null=True, max_length=100)
    slogan = models.CharField(verbose_name='分类标语', blank=True, null=True, max_length=100)
    bg_color = models.CharField(verbose_name='分类背景色', blank=True, null=True, max_length=10)
    is_recommended = models.BooleanField(verbose_name='是否首页推荐', default=False)

    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name
        db_table = 't_categories'
        ordering = ('-sort', '-add_time',)

    def __str__(self):
        return self.name
