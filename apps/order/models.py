from django.db import models

from apps.product.models import Spec, Product
from apps.user.models import User
from apps.logistics.models import LogisticsCompany, ShippingInfo
from apps.payment.models import PaymentMethod

from bigmarket.models import BaseModel
from bigmarket.choices import Choices


# 订单
class Order(BaseModel):
    """
    订单模型
    """
    creator = models.ForeignKey(User, verbose_name='创建人',
                                related_name='purchase_orders', on_delete=models.DO_NOTHING)
    order_no = models.CharField(verbose_name='订单号', default='', max_length=30)
    consignee = models.ForeignKey(ShippingInfo, verbose_name='收件人信息',
                                  related_name='be_consignee_orders', on_delete=models.DO_NOTHING)
    consignor = models.ForeignKey(ShippingInfo, verbose_name='发件人信息',
                                  related_name='be_consignor_orders', on_delete=models.DO_NOTHING)
    note = models.CharField(verbose_name='订单备注', default='', max_length=255)
    express = models.ForeignKey(LogisticsCompany, verbose_name='快递公司', on_delete=models.DO_NOTHING)
    tracking_no = models.CharField(verbose_name='物流追踪号', default='', max_length=100)
    payment = models.ForeignKey(PaymentMethod, verbose_name='支付方式', on_delete=models.DO_NOTHING)
    order_status = models.CharField(verbose_name='订单状态', default='', max_length=20,
                                    choices=Choices.ORDER_STATUS_CHOICES)
    payment_status = models.CharField(verbose_name='支付状态', default='', max_length=20,
                                      choices=Choices.PAYMENT_STATUS_CHOICES)
    premium = models.DecimalField(verbose_name='溢价', max_digits=18, decimal_places=2)
    promotion = models.DecimalField(verbose_name='优惠', max_digits=18, decimal_places=2)
    use_balance = models.DecimalField(verbose_name='使用余额', max_digits=18, decimal_places=2)
    total_price = models.DecimalField(verbose_name='总金额', max_digits=18, decimal_places=2)
    total_quantity = models.IntegerField(verbose_name='总商品数', default=0)

    def __str__(self):
        return self.order_no

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name
        db_table = 't_orders'
        ordering = ('-add_time',)


# 订单产品记录
class OrderRecord(BaseModel):
    """
    订单中的产品项
    """
    order = models.ForeignKey(Order, verbose_name='所属订单', on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, verbose_name='所购商品', on_delete=models.DO_NOTHING, related_name='orders')
    spec = models.ForeignKey(Spec, verbose_name='所购型号', on_delete=models.DO_NOTHING)
    price = models.DecimalField(verbose_name='价格', max_digits=18, decimal_places=2, default=0)
    quantity = models.DecimalField(verbose_name='购买数量', max_digits=18, decimal_places=2)
    unit_promotion = models.DecimalField(verbose_name='针对某个产品的优惠', max_digits=18, decimal_places=2)

    def __str__(self):
        return self.order.order_no + ' - ' + self.product.name

    class Meta:
        verbose_name = '订单记录'
        verbose_name_plural = verbose_name
        db_table = 't_order_Records'
        ordering = ('-add_time',)


# 售后服务记录
class AfterSalesRecord(BaseModel):
    """
    售后模型
    """
    order = models.ForeignKey(Order, verbose_name='相关订单',
                              on_delete=models.DO_NOTHING, related_name='after_sales_records')
    order_record = models.ForeignKey(OrderRecord, verbose_name='相关订单记录', on_delete=models.DO_NOTHING)
    creator = models.ForeignKey(User, verbose_name='创建人',
                                related_name='after_sales_demands', on_delete=models.DO_NOTHING)
    status = models.CharField(verbose_name='售后状态', default='', max_length=20,
                              choices=Choices.AFTER_SALES_STATUS_CHOICES)
    demand = models.CharField(verbose_name='售后要求', default='', max_length=20,
                              choices=Choices.AFTER_SALES_DEMAND_CHOICES)
    reason = models.TextField(verbose_name='售后理由', default='')
    quantity = models.PositiveIntegerField(verbose_name='申请售后产品数量', default=0)
    amount = models.DecimalField(verbose_name='申请退款金额', max_digits=18, decimal_places=2)
    message = models.TextField(verbose_name='处理备注', default='')
    need_return = models.BooleanField(verbose_name='是否要求客户退货', default=False)
    shipping_info = models.ForeignKey(ShippingInfo, verbose_name='退货地址', on_delete=models.DO_NOTHING)
    express = models.ForeignKey(LogisticsCompany, verbose_name='快递公司', on_delete=models.DO_NOTHING)
    tracking_no = models.CharField(verbose_name='物流追踪号', default='', max_length=100)

    class Meta:
        verbose_name='售后记录'
        verbose_name_plural = verbose_name
        db_table = 't_after_sales_records'
        ordering = ('-add_time',)


# 订单状态历史记录
class OrderStatusHistory(BaseModel):
    """
    订单状态变更记录
    """
    order = models.ForeignKey(Order, verbose_name='相关订单', on_delete=models.DO_NOTHING,
                              related_name='histories')
    previous_status = models.CharField(verbose_name='前一个状态', default='', max_length=20,
                                       choices=Choices.ORDER_STATUS_CHOICES)
    current_status = models.CharField(verbose_name='前一个状态', default='', max_length=20,
                                      choices=Choices.ORDER_STATUS_CHOICES)
    message = models.CharField(verbose_name='变更原因', default='', max_length=200)
    note = models.TextField(verbose_name='状态变更备注', default='')
    creator = models.ForeignKey(User, verbose_name='引起订单状态变更的用户', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = '订单状态变更记录'
        verbose_name_plural = verbose_name
        db_table = 't_order_status_history'
        ordering = ('-add_time',)


# 售后状态历史记录
class AfterSalesStatusHistory(BaseModel):
    """
    售后状态变更记录
    """
    after_sales_record = models.ForeignKey(AfterSalesRecord, verbose_name='相关售后',
                                           on_delete=models.DO_NOTHING, related_name='histories')
    previous_status = models.CharField(verbose_name='前一个状态', default='', max_length=20,
                                       choices=Choices.AFTER_SALES_STATUS_CHOICES)
    current_status = models.CharField(verbose_name='前一个状态', default='', max_length=20,
                                      choices=Choices.AFTER_SALES_STATUS_CHOICES)
    message = models.CharField(verbose_name='变更原因', default='', max_length=200)
    note = models.TextField(verbose_name='状态变更备注', default='')
    creator = models.ForeignKey(User, verbose_name='引起订单状态变更的用户', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = '售后记录状态变更历史'
        verbose_name_plural = verbose_name
        db_table = 't_after_sales_status_history'
        ordering = ('-add_time',)
