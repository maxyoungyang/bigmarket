from django.db import models

from apps.logistics.models import Region
from apps.user.models import User
from bigmarket.models import BaseModel
from bigmarket.choices import Choices


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


# 商品
class Product(BaseModel):
    """
    产品模型
    先按照指定优先级降序排列
    再按照创建时间降序排列
    """
    owner = models.ForeignKey(User, verbose_name='创建该产品的用户', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, verbose_name='产品品牌', blank=True, null=True, default=0,
                              on_delete=models.DO_NOTHING)
    category = models.ManyToManyField(Category, verbose_name='产品所属分类', related_name='products')
    name = models.CharField(verbose_name='产品名称', max_length=80)
    item_no = models.CharField(verbose_name='货号', default='', max_length=30, blank=True, null=True)
    brief = models.CharField(verbose_name='产品简述', blank=True, null=True, max_length=160)
    desc = models.TextField(verbose_name='产品描述', blank=True, null=True)
    is_id_needed = models.BooleanField(verbose_name='是否需要ID', default=False)

    place_origin = models.ForeignKey(Region, verbose_name='产地', on_delete=models.DO_NOTHING,
                                     related_name='origin_products', db_column='origin_id', blank=True, null=True)
    place_delivery = models.ForeignKey(Region, verbose_name='发货地', on_delete=models.DO_NOTHING,
                                       related_name='delivery_products', db_column='delivery_id', blank=True, null=True)

    access_count = models.PositiveIntegerField(verbose_name='浏览次数', default=0)
    like_count = models.PositiveIntegerField(verbose_name='点赞次数', default=0)
    favorite_count = models.PositiveIntegerField(verbose_name='收藏次数', default=0)

    is_recommended = models.BooleanField('是否首页推荐', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name
        db_table = 't_products'
        ordering = ('-sort', '-add_time')


# 商品规格
class Spec(BaseModel):
    """
    产品规格模型
    先按照指定优先级降序排列
    再按照创建时间降序排列
    """
    product = models.ForeignKey(Product, verbose_name='所属产品', on_delete=models.CASCADE, related_name='specs')
    parent = models.ForeignKey('self', verbose_name='父级规格',
                               on_delete=models.CASCADE, related_name='children', db_column='pid')
    name = models.CharField(verbose_name='规格名称', max_length=30)
    value = models.CharField(verbose_name='规格值', max_length=30)

    class Meta:
        verbose_name = '商品规格'
        verbose_name_plural = verbose_name
        ordering = ('-sort', '-add_time')
        db_table = 't_specs'


# 规格细节
class SpecDetail(BaseModel):
    """
    产品规格细节模型
    """
    spec = models.OneToOneField(Spec, verbose_name='所属产品', on_delete=models.CASCADE, related_name='detail')
    note = models.CharField(verbose_name='规格说明', blank=True, null=True, max_length=160)

    gross_weight = models.DecimalField(verbose_name='毛重(g)', max_digits=10, decimal_places=2,
                                       default=0, blank=True, null=True)
    length = models.IntegerField(verbose_name='长(mm)', default=0, blank=True, null=True)
    height = models.IntegerField(verbose_name='高(mm)', default=0, blank=True, null=True)
    width = models.IntegerField(verbose_name='宽(mm)', default=0, blank=True, null=True)

    sku = models.CharField(verbose_name='规格编码', max_length=80, default='', blank=True, null=True)
    barcode = models.CharField(verbose_name='条形码', max_length=80, default='', blank=True, null=True)

    min_quantity = models.IntegerField(verbose_name='最小可购买数量', default=0)
    max_quantity = models.IntegerField(verbose_name='最大可购买数量', default=0)

    inventory = models.IntegerField(verbose_name='库存数量', default=0)
    is_deduction_inventory = models.BooleanField(verbose_name='是否扣减库存', default=False)

    class Meta:
        verbose_name = '规格详情'
        verbose_name_plural = verbose_name
        ordering = ('-sort', '-add_time')
        db_table = 't_spec_details'


# 库存变化记录
class InventoryHistory(BaseModel):
    """
    库存变更记录
    """
    spec = models.ForeignKey(Spec, verbose_name='相关规格', on_delete=models.DO_NOTHING)
    change = models.IntegerField(verbose_name='变化数量', default=0)
    current_inventory = models.IntegerField(verbose_name='变化后', default=0)
    message = models.CharField(verbose_name='变更原因', default='', max_length=200)
    note = models.TextField(verbose_name='库存变更备注', default='')
    creator = models.ForeignKey(User, verbose_name='引起库存变更的用户', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.spec.product.name + ' - ' + self.spec.name + ' - '\
               + str(self.change) + ' - ' + str(self.current_inventory)

    class Meta:
        verbose_name = '库存变化记录'
        verbose_name_plural = verbose_name
        db_table = 't_inventory_histories'
        ordering = ('-add_time',)


# 用户互动商品
class InteractedProduct(BaseModel):
    user = models.ForeignKey(User, verbose_name='所属用户',
                             on_delete=models.DO_NOTHING, related_name='interacted_products')
    product = models.ForeignKey(Product, verbose_name='相关商品',
                                on_delete=models.DO_NOTHING, related_name='users')
    type = models.CharField(verbose_name='行为', max_length=20, choices=Choices.INTERACTED_PRODUCT_TYPE_CHOICES)

    def __str__(self):
        return self.product.name + ' - ' + self.user.mobile

    class Meta:
        verbose_name = '互动商品记录'
        verbose_name_plural = verbose_name
        db_table = 't_interacted_products'
        ordering = ('-add_time',)


# 用户在售规格
class AvailableSpec(BaseModel):
    user = models.ForeignKey(User, verbose_name='所属用户',
                             on_delete=models.DO_NOTHING, related_name='available_specs')
    spec = models.ForeignKey(Spec, verbose_name='相关规格',
                             on_delete=models.DO_NOTHING, related_name='users')

    def __str__(self):
        return self.spec.name + ' - ' + self.user.mobile

    class Meta:
        verbose_name = '可售规格记录'
        verbose_name_plural = verbose_name
        db_table = 't_available_specs'
        ordering = ('-add_time',)
