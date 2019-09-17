import xadmin

from .models import Region
# 需要import要管理的model类

class RegionAdmin(object):
    list_display = ['id', 'name', 'level', 'parent', 'is_enable']  # 列表页中要显示的字段
    search_fields = ['name']  # 支持查找的字段（可以模糊查找）
    list_filter = ['id', 'name', 'level', 'parent', 'is_enable', 'add_time']  # 可以使用过滤器的字段
    list_editable = ['name', 'level', 'parent', 'is_enable', 'add_time']  # 可以在列表页中编辑的字段


# 模型注册，第一个参数为模型对象，第二个参数是上面编写好的管理器类
xadmin.site.register(Region, RegionAdmin)