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


# 用户互动内容
class InteractedArticle(BaseModel):
    user = models.ForeignKey(User, verbose_name='所属用户',
                             on_delete=models.DO_NOTHING, related_name='interacted_articles')
    article = models.ForeignKey(Articles, verbose_name='相关商品',
                                on_delete=models.DO_NOTHING, related_name='users')
    type = models.CharField(verbose_name='行为', max_length=20, choices=Choices.INTERACTED_CONTENT_TYPE_CHOICES)

    def __str__(self):
        return self.article.title + ' - ' + self.user.mobile

    class Meta:
        verbose_name = '互动内容记录'
        verbose_name_plural = verbose_name
        db_table = 't_interacted_articles'
        ordering = ('-add_time',)
