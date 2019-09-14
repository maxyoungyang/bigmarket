from django.db import models

from apps.community.models import Articles
from apps.product.models import Spec
from bigmarket.models import BaseMedia
from bigmarket.choices import Choices


class ProductMedia(BaseMedia):
    position = models.CharField(verbose_name='媒体位置', max_length=10, choices=Choices.PRODUCT_MEDIA_POSITION_CHOICES)
    belong_to = models.ForeignKey(Spec, verbose_name='所属规格', on_delete=models.DO_NOTHING, related_name='medias')
    image = models.ImageField(verbose_name="图片", upload_to="media/image/product", null=True, blank=True)
    video = models.FileField(verbose_name="视频", upload_to="media/video/product", null=True, blank=True)

    class Meta:
        verbose_name = '商品媒体'
        verbose_name_plural = verbose_name
        db_table = 't_product_medias'
        ordering = ('-sort', '-add_time',)


class ArticlesMedia(BaseMedia):
    belong_to = models.ForeignKey(Articles, verbose_name='所属规格', on_delete=models.DO_NOTHING, related_name='medias')
    image = models.ImageField(verbose_name="图片", upload_to="media/image/article", null=True, blank=True)
    video = models.FileField(verbose_name="视频", upload_to="media/video/article", null=True, blank=True)

    class Meta:
        verbose_name = '文章媒体'
        verbose_name_plural = verbose_name
        db_table = 't_articles_medias'
        ordering = ('-sort', '-add_time',)


class SystemMedia(BaseMedia):
    position = models.CharField(verbose_name='媒体位置', max_length=10, choices=Choices.SYSTEM_MEDIA_POSITION_CHOICES)
    image = models.ImageField(verbose_name="图片", upload_to="media/image/system", null=True, blank=True)
    video = models.FileField(verbose_name="视频", upload_to="media/video/system", null=True, blank=True)
    link = models.CharField(verbose_name='链接', max_length=200, default='')

    class Meta:
        verbose_name = '系统媒体'
        verbose_name_plural = verbose_name
        db_table = 't_system_medias'
        ordering = ('-sort', '-add_time',)
