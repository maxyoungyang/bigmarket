from django.db import models

from apps.user.models import User
from bigmarket.models import BaseModel
from bigmarket.choices import Choices


class Articles(BaseModel):
    announcer = models.ForeignKey(User, verbose_name='发布人',
                                  related_name='outbox', on_delete=models.DO_NOTHING)
    recipient = models.ForeignKey(User, verbose_name='收信人', null=True, blank=True,
                                  related_name='inbox', on_delete=models.DO_NOTHING)
    belong_to = models.PositiveIntegerField(verbose_name='属于对象', null=True, blank=True)
    title = models.CharField(verbose_name='标题', default='', max_length=80, null=True, blank=True)
    content = models.TextField(verbose_name='内容', default='', null=True, blank=True)
    type = models.CharField(verbose_name='文章类型', default='', max_length=10, choices=Choices.ARTICLE_TYPE_CHOICES)

    class Meta:
        verbose_name = '文章/消息'
        verbose_name_plural = verbose_name
        db_table = 't_articles'
        ordering = ('-sort', '-add_time',)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return self.content


