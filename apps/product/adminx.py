import xadmin

from .models import Brand, Category, Product, Spec, SpecDetail, InventoryHistory, InteractedProduct, ProductSalesType, \
    AvailableSpec


# 需要import要管理的model类

class BrandAdmin(object):
    list_display = ['creator', 'name', 'letter', 'is_recommended']  # 列表页中要显示的字段
    search_fields = ['name', 'letter']  # 支持查找的字段（可以模糊查找）
    list_filter = ['creator', 'name', 'letter', 'is_recommended']  # 可以使用过滤器的字段
    list_editable = ['is_recommended']  # 可以在列表页中编辑的字段

# 模型注册，第一个参数为模型对象，第二个参数是上面编写好的管理器类
xadmin.site.register(Brand, BrandAdmin)


# class CategoryAdmin(object):
#     # list_display = ['', ]  # 列表页中要显示的字段
#     # search_fields = ['', ]  # 支持查找的字段（可以模糊查找）
#     # list_filter = ['', ]  # 可以使用过滤器的字段
#     # list_editable = ['', ]  # 可以在列表页中编辑的字段
#
# # 模型注册，第一个参数为模型对象，第二个参数是上面编写好的管理器类
# xadmin.site.register(Category, CategoryAdmin)
#
#
# class ProductAdmin(object):
#     # list_display = ['', ]  # 列表页中要显示的字段
#     # search_fields = ['', ]  # 支持查找的字段（可以模糊查找）
#     # list_filter = ['', ]  # 可以使用过滤器的字段
#     # list_editable = ['', ]  # 可以在列表页中编辑的字段
#
# # 模型注册，第一个参数为模型对象，第二个参数是上面编写好的管理器类
# xadmin.site.register(Product, ProductAdmin)
#
#
# class SpecAdmin(object):
#     # list_display = ['', ]  # 列表页中要显示的字段
#     # search_fields = ['', ]  # 支持查找的字段（可以模糊查找）
#     # list_filter = ['', ]  # 可以使用过滤器的字段
#     # list_editable = ['', ]  # 可以在列表页中编辑的字段
#
# # 模型注册，第一个参数为模型对象，第二个参数是上面编写好的管理器类
# xadmin.site.register(Spec, SpecAdmin)
#
#
# class SpecDetailAdmin(object):
#     list_display = ['', ]  # 列表页中要显示的字段
#     search_fields = ['', ]  # 支持查找的字段（可以模糊查找）
#     list_filter = ['', ]  # 可以使用过滤器的字段
#     list_editable = ['', ]  # 可以在列表页中编辑的字段
#
# # 模型注册，第一个参数为模型对象，第二个参数是上面编写好的管理器类
# xadmin.site.register(SpecDetail, SpecDetailAdmin)
#
#
# class InventoryHistoryAdmin(object):
#     list_display = ['', ]  # 列表页中要显示的字段
#     search_fields = ['', ]  # 支持查找的字段（可以模糊查找）
#     list_filter = ['', ]  # 可以使用过滤器的字段
#     list_editable = ['', ]  # 可以在列表页中编辑的字段
#
# # 模型注册，第一个参数为模型对象，第二个参数是上面编写好的管理器类
# xadmin.site.register(InventoryHistory, InventoryHistoryAdmin)
#
#
# class InteractedProductAdmin(object):
#     list_display = ['', ]  # 列表页中要显示的字段
#     search_fields = ['', ]  # 支持查找的字段（可以模糊查找）
#     list_filter = ['', ]  # 可以使用过滤器的字段
#     list_editable = ['', ]  # 可以在列表页中编辑的字段
#
# # 模型注册，第一个参数为模型对象，第二个参数是上面编写好的管理器类
# xadmin.site.register(InteractedProduct, InteractedProductAdmin)
#
#
# class ProductSalesTypeAdmin(object):
#     # list_display = ['', ]  # 列表页中要显示的字段
#     # search_fields = ['', ]  # 支持查找的字段（可以模糊查找）
#     # list_filter = ['', ]  # 可以使用过滤器的字段
#     # list_editable = ['', ]  # 可以在列表页中编辑的字段
#
# # 模型注册，第一个参数为模型对象，第二个参数是上面编写好的管理器类
# xadmin.site.register(ProductSalesType, ProductSalesTypeAdmin)
#
#
# class AvailableSpecAdmin(object):
#     # list_display = ['', ]  # 列表页中要显示的字段
#     # search_fields = ['', ]  # 支持查找的字段（可以模糊查找）
#     # list_filter = ['', ]  # 可以使用过滤器的字段
#     # list_editable = ['', ]  # 可以在列表页中编辑的字段
#
# # 模型注册，第一个参数为模型对象，第二个参数是上面编写好的管理器类
# xadmin.site.register(AvailableSpec, AvailableSpecAdmin)

