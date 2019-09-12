"""
定义系统的配置参数
"""


class Choices(object):
    """
    系统需要的常量参数
    """
    # 性别
    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
    ]
    # 订单状态
    ORDER_STATUS_CHOICES = [
        ('cart', '购物车'),
        ('confirmed', '已确认'),
        ('processing', '处理中'),
        ('shipped', '已发货'),
        ('finished', '已完结'),
        ('after_sales', '发生售后'),
        ('cancelled', '已取消'),
    ]
    # 支付状态
    PAYMENT_STATUS_CHOICES = [
        ('unpaid', '未支付'),  #
        ('paid', '已支付'),  # 用户已经确认的订单，但还没有付款
    ]
    # 支付方式
    PAYMENT_METHOD_CHOICES = [
        ('balance', '余额支付'),
        ('wechat', '微信支付'),
        ('alipay', '支付宝'),
        ('debit_card', '银行卡'),
        ('credit_card', '信用卡'),
        ('applepay', 'applypay'),
        ('paypal', 'paypal'),
    ]
    # 三方支付
    THIRD_PART_PAYMENT_CHOICES = [
        ('wechat', '微信支付'),
        ('alipay', '支付宝'),
        ('allinpay', '通联支付'),
    ]
    # 售后状态
    AFTER_SALES_STATUS_CHOICES = [
        ('confirming', '等待卖家确认'),
        ('returning', '等待退货'),
        ('refunding', '等待退款'),
        ('refunded', '已退款'),
        ('refused', '卖家拒绝'),
        ('finished', '已完成售后'),
        ('cancelled', '买家取消售后请求'),
    ]
    # 售后要求
    AFTER_SALES_DEMAND_CHOICES = [
        ('return', '退货退款'),
        ('refund', '直接退款'),
        ('part_refund', '部分退款'),
        ('change', '更换商品'),
    ]
    # 退款方式
    REFUND_METHOD_CHOICES = [
        ('original', '原路退回'),
        ('balance', '退回余额'),
        ('offline', '线下退款'),
    ]
    # 销售方式
    SALES_TYPE_CHOICES = [
        ('wr', '供货和零售'),
        ('w', '只供货'),
        ('r', '只零售'),
    ]
    # 用户状态
    USER_STATUS_CHOICES = [
        ('new', '新用户'),
        ('normal', '正常'),
        ('lp', '限制购买'),
        ('lw', '限制提款'),
        ('al', '限制全部功能'),
        ('frozen', '冻结'),
    ]
    # 用户等级
    USER_LEVEL_CHOICES = [
        ('normal', '普通用户'),
        ('vip', '高级用户'),
    ]
    # 媒体类型
    MEDIA_TYPE_CHOICES = [
        ('image', '图片'),
        ('video', '视频'),
        ('text', '文本'),
    ]
    # 平台类型
    USE_FOR_CHOICES = [
        ('web', 'web网站'),
        ('h5', 'H5'),
        ('ios', 'IOS'),
        ('android', 'ANDROID'),
        ('wechat_mp', '微信小程序'),
        ('alipay_mp', '支付宝小程序'),
        ('baidu_mp', '百度小程序'),
    ]
    # 文章类型
    ARTICLE_TYPE_CHOICES = [
        ('detail', '图文详情'),
        ('ad', '广告素材'),
        ('blog', '文章'),
        ('public', '系统公告'),
        ('message', '私信'),
    ]
    # 电子货币类型
    CURRENCY_TYPE_CHOICES = [
        ('balance', '余额'),
        ('integral', '积分'),
        ('financial', '理财'),
    ]
