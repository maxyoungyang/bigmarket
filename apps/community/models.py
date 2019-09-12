from django.db import models

from apps.user.models import User
from bigmarket.models import BaseModel
from bigmarket.choices import Choices


# 文章素材
class Articles(BaseModel):
    belong_to = models.PositiveIntegerField(verbose_name='属于对象', null=True, blank=True)
    title = models.CharField(verbose_name='标题', default='', max_length=80, null=True, blank=True)
    content = models.TextField(verbose_name='内容', default='', null=True, blank=True)
    type = models.CharField(verbose_name='文章类型', default='', max_length=10, choices=Choices.ARTICLE_TYPE_CHOICES)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        db_table = 't_articles'
        ordering = ('-sort', '-add_time',)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return self.content


# 用户消息
class Message(BaseModel):
    announcer = models.ForeignKey(User, verbose_name='发布人',
                                  related_name='outbox', on_delete=models.DO_NOTHING)
    recipient = models.ForeignKey(User, verbose_name='收信人', null=True, blank=True,
                                  related_name='inbox', on_delete=models.DO_NOTHING)
    title = models.CharField(verbose_name='标题', default='', max_length=80, null=True, blank=True)
    content = models.TextField(verbose_name='内容', default='', null=True, blank=True)
    is_topping = models.BooleanField(verbose_name='是否置顶', default=False)

    class Meta:
        verbose_name = '消息'
        verbose_name_plural = verbose_name
        db_table = 't_messages'
        ordering = ('-sort', '-add_time',)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return self.content


class Media(BaseModel):
    """
    媒体模型
    按给定优先级'sort'排序
    """
    belong_to = models.PositiveIntegerField(verbose_name='归属对象')
    owner_type = models.CharField(verbose_name='归属对象类型', max_length=20)
    use_for = models.CharField(verbose_name='用途', max_length=20)
    filename = models.CharField(verbose_name='文件名', max_length=200)
    type = models.CharField(verbose_name='媒体类型', max_length=10, choices=Choices.MEDIA_TYPE_CHOICES)
    image = models.ImageField(verbose_name="图片", upload_to="media/image/", null=True, blank=True)
    video = models.FileField(verbose_name="视频", upload_to="media/video/", null=True, blank=True)
    content = models.TextField(verbose_name='文本', null=True, blank=True)

    def __str__(self):
        return self.filename

    class Meta:
        verbose_name = '媒体'
        verbose_name_plural = verbose_name
        db_table = 't_medias'
        ordering = ('-sort', '-add_time')
