"""
设置模块名称
"""
from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'apps.user'
    verbose_name = '用户管理'
