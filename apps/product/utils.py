"""
产品模块相关业务逻辑
"""
import math

import hashlib
import time

from django.db import transaction

from apps.logistics.models import Region
from apps.pricing.utils import create_pricing
from apps.product.models import Category, Product, Spec, Brand, SpecDetail, ProductSalesType, ProductCategory, \
    AvailableSpec
from apps.user.models import User
from bigmarket.commonutils import get_xls_table, is_empty, is_number
from exception.custom_exception import ImportProductsException


def get_min_max_quantity(text):
    """
    获得阶梯价格一档的最小和最大定量
    :param text: 格式: "最小起订量-最大起订量"
    :return:
    """
    min_max_numbers = [0, 0]
    if is_empty(text) is False:
        min_max_list = str(text).split('-')
        if len(min_max_list) == 2 and \
                is_number(min_max_list[0].strip()) is True and \
                is_number(min_max_list[1].strip()) is True and \
                math.modf(float(min_max_list[0]))[0] == 0 and \
                math.modf(float(min_max_list[1]))[0] == 0 and \
                int(min_max_list[1]) > int(min_max_list[0]) > 0:
            min_max_numbers[0] = int(min_max_list[0])
            min_max_numbers[1] = int(min_max_list[1])
            return min_max_numbers
        else:
            if len(min_max_list) == 1 and \
                    is_number(min_max_list[0].strip()) is True and \
                    math.modf(float(min_max_list[0]))[0] == 0 and \
                    int(min_max_list[0]) > 0:
                min_max_numbers[0] = int(min_max_list[0])
                return min_max_numbers
            else:
                return "阶梯最大值最小值设置有误，请检查"
    return min_max_numbers


def create_brand(user, name):
    """
    创建品牌
    :param user:
    :param name:
    :return:
    """
    brand = Brand()
    brand.creator = user
    brand.name = name
    brand.save()
    return brand


def create_category(creator, parent_category, name):
    """
    创建分类
    :param creator:
    :param parent_category:
    :param name:
    :return:
    """
    category = Category()
    category.creator = creator
    category.name = name
    category.parent = parent_category
    if parent_category:
        category.level = parent_category.level + 1
    else:
        category.level = 1

    category.sort = 0
    category.is_delete = False
    category.is_enable = True
    category.save()
    return category


def create_product_category(product,
                            category=None,
                            first_category_name='',
                            second_category_name='',
                            third_category_name=''):
    """
    创建商品-分类关系对象
    :param product:
    :param category:
    :param first_category_name:
    :param second_category_name:
    :param third_category_name:
    :return:
    """
    pc = ProductCategory()
    pc.product = product
    if category is not None:
        pass
    else:
        # 设定商品分类，如果商品分类未创建，则创建分类，必须一级，二级，三级分类都有数据，否则被归入创建该商品的用户的系统默认分类
        if third_category_name is not None and third_category_name != '':  # 如果输入的商品三级分类名不是空字符串
            third_category_set = Category.objects.filter(name__exact=third_category_name)
            if len(third_category_set) > 0:  # 如果三级分类已存在
                category = third_category_set[0]
            else:
                if second_category_name is not None and second_category_name != '':
                    second_category_set = Category.objects.filter(name__exact=second_category_name)
                    if len(second_category_set) > 0:  # 如果二级分类已存在，则创建新的三级分类，并将产品分类设置为这个新的三级分类
                        category = create_category(product.creator, second_category_set[0], third_category_name)
                    else:  # 如果二级分类不存在，则查看一级分类
                        if first_category_name is not None and first_category_name != '':
                            first_category_set = Category.objects.filter(name__exact=first_category_name)
                            if len(first_category_set) > 0:
                                second_category = create_category(product.creator, first_category_set[0],
                                                                  second_category_name)
                                third_category = create_category(product.creator, second_category, third_category_name)
                                category = third_category
                            else:
                                first_category = create_category(product.creator, None, first_category_name)
                                second_category = create_category(product.creator, first_category, second_category_name)
                                third_category = create_category(product.creator, second_category, third_category_name)
                                category = third_category
                        else:
                            error_message = "商品分类必须完整填写三个等级的分类名称，不确定可以不填"
                            return error_message
                else:
                    error_message = "商品分类必须完整填写三个等级的分类名称，不确定可以不填"
                    return error_message
        else:
            category = Category.objects.filter(id=999)[0]
    pc.category = category
    pc_exits_set = ProductCategory.objects.filter(product=product, category=category)
    if len(pc_exits_set) > 0:
        pc = pc_exits_set[0]
    pc.sort = 0
    pc.is_delete = False
    pc.is_enable = True
    pc.save()
    return pc


def create_product(creator, name='', brief='', item_no='',
                   brand_id=0, place_origin='', place_delivery='',
                   is_id_needed=False, desc=''):
    """
    创建商品
    :param creator:
    :param name:
    :param brief:
    :param item_no:
    :param brand_id:
    :param place_origin:
    :param place_delivery:
    :param is_id_needed:
    :param desc:
    :return:
    """
    # 商品名称
    if name is None or name == '':
        error_message = "未填写商品名称"
        return error_message
    else:
        same_name_products = Product.objects.filter(name=name)
        if len(same_name_products) > 0:
            return same_name_products[0]
        else:
            product = Product()
            product.name = name

    # 商品创建人
    if creator is None:
        error_message = "没有指定商品的创建用户"
        return error_message
    else:
        product.creator = creator

    # 商品简述
    product.brief = brief

    # 商品货号
    duplicate_item_no_products = Product.objects.filter(item_no=item_no)
    if len(duplicate_item_no_products) > 0:
        error_message = "商品编码重复，请修正"
        return error_message
    if item_no is None or item_no == '':
        md5 = hashlib.md5()
        md5.update(name)
        product.item_no = md5.hexdigest()
    else:
        product.item_no = item_no

    if brand_id is not None and \
            brand_id != '' and \
            is_number(brand_id) and \
            brand_id > 0 and \
            math.modf(float(brand_id))[0] == 0:
        brand_set = Brand.objects.filter(id=brand_id)
        if len(brand_set) > 0:
            product.brand = brand_set[0]
        else:
            product.brand = None
    elif brand_id == '':
        product.brand = None
    else:
        error_message = "商品品牌ID填写错误，可能原因：非数字、不是整数、负数或0，请确认"
        return error_message

    # 设置原产地和发货地
    if len(Region.objects.filter(name=place_origin)) > 0:
        product.place_origin = Region.objects.filter(name=place_origin)[0]
    else:
        product.place_origin = None

    if len(Region.objects.filter(name=place_delivery)) > 0:
        product.place_delivery = Region.objects.filter(name=place_delivery)[0]
    else:
        product.place_delivery = None

    # 设置商品发货是否需要收件人身份证
    if is_id_needed:
        product.is_id_needed = True
    else:
        product.is_id_needed = False

    # 设置产品文字描述
    product.desc = desc

    product.save()

    return product


def create_spec(product, items=None, spec_no=''):
    """
    创建规格
    """
    spec = Spec()
    spec.product = product

    if items is None or len(items) == 0:
        spec.items = "{\'default\':\'default\'}"
    else:
        spec.items = items

    if spec_no is None or spec_no == '' or len(Spec.objects.filter(spec_no=spec_no)) > 0:
        spec_count = Spec.objects.filter(product=product).count()
        spec.spec_no = product.item_no + '-' + str(spec_count + 1)
    else:
        spec.spec_no = spec_no
    spec.save()
    return spec


def create_spec_detail(spec,
                       min_order_quantity=0,
                       max_order_quantity=0,
                       gross_weight=0,
                       length=0,
                       height=0,
                       width=0,
                       sku='',
                       barcode='',
                       inventory=0,
                       is_deduction_inventory=False,
                       note=''):
    """
    创建规格详情
    """
    spec_detail = SpecDetail()
    spec_detail.spec = spec
    # 设置最小起订量和最大订购量
    spec_detail.min_order_quantity = min_order_quantity
    spec_detail.max_order_quantity = max_order_quantity
    spec_detail.gross_weight = gross_weight
    spec_detail.length = length
    spec_detail.height = height
    spec_detail.width = width
    spec_detail.sku = sku
    spec_detail.barcode = barcode
    spec_detail.inventory = inventory
    spec_detail.is_deduction_inventory = is_deduction_inventory
    spec_detail.note = note
    spec_detail.save()
    return spec_detail


def create_available_spec(user, spec):
    """
    创建 AvailableSpec
    """
    available_spec = AvailableSpec()
    available_spec.user = user
    available_spec.spec = spec
    available_spec.save()
    return available_spec


def create_product_sales_type(user, product, is_wholesale=True, is_retail=True):
    """
    创建 ProductSalesType
    """
    product_sales_type_exist_set = ProductSalesType.objects.filter(user=user, product=product)
    if len(product_sales_type_exist_set) > 0:
        product_sales_type = product_sales_type_exist_set[0]
    else:
        product_sales_type = ProductSalesType()
        product_sales_type.user = user
        product_sales_type.product = product
    if is_wholesale:
        if is_retail:
            product_sales_type.type = 'wr'
        else:
            product_sales_type.type = 'w'
    else:
        if is_retail:
            product_sales_type.type = 'r'
        else:
            return '销售模式设置错误'
    product_sales_type.save()
    return product_sales_type


def import_multi_products(filepath):
    """
    通过xls文件批量导入产品信息
    """
    table = get_xls_table(filepath)
    rows_count = table.nrows  # 取总行数

    errors_dict = {}
    for row_index in range(1, rows_count):  # 行循环
        error_message = ''
        row_data = table.row_values(row_index)
        try:
            with transaction.atomic():
                # *** 先检测必填项 ***
                if row_data[0] is None or row_data[0] == '' or is_number(row_data[0]) \
                        is False or math.modf(float(row_data[0]))[0] > 0 or float(row_data[0]) < 1:
                    error_message = \
                        "第{row_index}行导入失败，原因：第A列，创建用户ID不正确".format(row_index=row_index)
                    raise ImportProductsException()
                if row_data[1] is None or row_data[1] == '':
                    error_message = \
                        "第{row_index}行导入失败，原因：第B列，标题名称为必填项，未填写".format(row_index=row_index)
                    raise ImportProductsException()
                if is_number(row_data[9]) is False or (float(row_data[9]) != 0 and float(row_data[9]) != 1):
                    error_message = "第{row_index}行导入失败，原因：第G列，必填且只能填写0或者1,0代表不需要，1代表需要"\
                        .format(row_index=row_index)
                    raise ImportProductsException()
                if row_data[19] is None or row_data[19] == '' or row_data[19].strip().upper() not in \
                        'CNY CNH CAD USD AUD NZD EUR JPY GBP HKD KRW' or str(row_data[19].strip()).__len__() != 3:
                    error_message = \
                        "第{row_index}行导入失败，原因：第T列，商品计价币种填写错误".format(row_index=row_index)
                    raise ImportProductsException()

                if is_number(row_data[21]) is False or float(row_data[21]) < 0:
                    error_message = \
                        "第{row_index}行导入失败，原因：第V列，至少需要设置正确的价格1".format(row_index=row_index)
                    raise ImportProductsException()

                if is_number(row_data[28]) is False or (float(row_data[28]) != 0 and float(row_data[28]) != 1):
                    error_message = \
                        "第{row_index}行导入失败，原因：第AC列，只能填写0或者1,0代表不包邮，1代表包邮".format(row_index=row_index)
                    raise ImportProductsException()
                # *** END ***

                # *** 创建商品对象 ***
                # 根据商品货号进行查找，如果该商品已存在，则从数据库中取出，如果不存在则创建新商品
                product_set = Product.objects.filter(item_no=row_data[3])
                if len(product_set) == 0:
                    # 获得创建商品用户
                    user_set = User.objects.filter(id=row_data[0])
                    if len(user_set) > 0:
                        creator = user_set[0]
                    else:
                        error_message = \
                            "第{row_index}行导入失败，原因：第A列，创建用户ID不正确".format(row_index=row_index)
                        raise ImportProductsException()
                    # 获得商品简述
                    name = row_data[1]
                    brief = row_data[2]
                    item_no = row_data[3]
                    brand_id = row_data[7]
                    place_delivery = row_data[8]
                    is_id_needed = False
                    if int(row_data[9]) == 1:
                        is_id_needed = True

                    desc = row_data[40]
                    product = create_product(creator,
                                             name=name,
                                             brief=brief,
                                             item_no=item_no,
                                             brand_id=brand_id,
                                             place_delivery=place_delivery,
                                             is_id_needed=is_id_needed,
                                             desc=desc)
                    if type(product) == str:
                        error_message = "第{row_index}行导入失败，原因：{error_message}"\
                            .format(row_index=row_index, error_message=product)
                        raise ImportProductsException()
                else:
                    product = product_set[0]
                # *** END ***

                # *** 设置分类关系 ***
                first_category_name = row_data[4]
                second_category_name = row_data[5]
                third_category_name = row_data[6]
                product_category = create_product_category(product,
                                                           first_category_name=first_category_name,
                                                           second_category_name=second_category_name,
                                                           third_category_name=third_category_name)
                if type(product_category) == str:
                    error_message = "第{row_index}行导入失败，原因：{error_message}" \
                        .format(row_index=row_index, error_message=product_category)
                    raise ImportProductsException()
                # *** END ***

                # *** 保存新规格 ***
                items = {}
                if row_data[12] == '' and row_data[13] == '' and row_data[14] == '' and row_data[15] == '' and \
                        row_data[16] == '' and row_data[17] == '':
                    pass
                else:
                    # 加入一级规格
                    if row_data[12] != '' and row_data[13] != '':
                        items[row_data[12]] = row_data[13]
                    # 加入二级规格
                    if row_data[14] != '' and row_data[15] != '':
                        items[row_data[14]] = row_data[15]
                    # 加入三级规格
                    if row_data[16] != '' and row_data[17] != '':
                        items[row_data[16]] = row_data[17]
                spec_no = row_data[18]
                if len(Spec.objects.filter(spec_no=spec_no)) > 0:
                    error_message = "第{row_index}行导入失败，原因：第S列，规格编码重复，请修正，不填则系统会自动分配一个唯一编码" \
                        .format(row_index=row_index)
                    raise ImportProductsException()

                spec = create_spec(product, items, spec_no)
                if type(spec) == str:
                    error_message = \
                        "第{row_index}行导入失败，原因：{error_message}".format(row_index=row_index, error_message=spec)
                    raise ImportProductsException()
                spec.save()
                # *** END ***

                # *** 创建规格详情 ***
                if row_data[10] is not None and row_data[10] != '':
                    if is_number(row_data[10]):
                        min_order_quantity = int(row_data[10])
                    else:
                        error_message = "第{row_index}行导入失败，原因：第K列，最小起订量必须是正整数" \
                            .format(row_index=row_index)
                        raise ImportProductsException()
                else:
                    min_order_quantity = 1

                if row_data[11] is not None and row_data[11] != '':
                    if is_number(row_data[11]):
                        max_order_quantity = int(row_data[11])
                        if max_order_quantity < min_order_quantity:
                            error_message = \
                                "第{row_index}行导入失败，原因：第L列，最大订购量必须是正整数".format(row_index=row_index)
                            raise ImportProductsException()
                    else:
                        error_message = \
                            "第{row_index}行导入失败，原因：第L列，最大订购量必须大于等于最小起订量".format(row_index=row_index)
                        raise ImportProductsException()
                else:
                    max_order_quantity = 9999

                note = row_data[38]

                if (is_empty(row_data[30]) is False and is_number(row_data[30]) is False) or (
                        is_number(row_data[30]) is True and float(row_data[30]) <= 0):
                    error_message = \
                        "第{row_index}行导入失败，原因：第AE列，毛重必须为数字，且大于0，非必填".format(row_index=row_index)
                    raise ImportProductsException()
                if is_empty(row_data[30]) is False:
                    gross_weight = float(row_data[30])
                else:
                    gross_weight = 0

                if (is_empty(row_data[31]) is False and is_number(row_data[31]) is False) or (
                        is_number(row_data[31]) is True and float(row_data[31]) <= 0):
                    error_message = \
                        "第{row_index}行导入失败，原因：第AF列，长必须为数字，且大于0，非必填".format(row_index=row_index)
                    raise ImportProductsException()
                if is_empty(row_data[31]) is False:
                    length = float(row_data[31])
                else:
                    length = 0

                if (is_empty(row_data[32]) is False and is_number(row_data[32]) is False) or (
                        is_number(row_data[32]) is True and float(row_data[32]) <= 0):
                    error_message = \
                        "第{row_index}行导入失败，原因：第AG列，宽度必须为数字，且大于0，非必填".format(row_index=row_index)
                    raise ImportProductsException()
                if is_empty(row_data[32]) is False:
                    width = float(row_data[32])
                else:
                    width = 0

                if (is_empty(row_data[33]) is False and is_number(row_data[33]) is False) or (
                        is_number(row_data[33]) is True and float(row_data[33]) <= 0):
                    error_message = \
                        "第{row_index}行导入失败，原因：第AH列，高度必须为数字，且大于0，非必填".format(row_index=row_index)
                    raise ImportProductsException()
                if is_empty(row_data[33]) is False:
                    height = float(row_data[33])
                else:
                    height = 0

                sku = row_data[34]
                barcode = row_data[35]

                if is_empty(row_data[36]) is False and is_number(row_data[36]) is True and int(row_data[36]) >= 0:
                    inventory = int(row_data[36])
                    is_deduction_inventory = True
                else:
                    inventory = 9999
                    is_deduction_inventory = False

                spec_detail = create_spec_detail(spec,
                                                 min_order_quantity=min_order_quantity,
                                                 max_order_quantity=max_order_quantity,
                                                 gross_weight=int(gross_weight),
                                                 length=int(length),
                                                 height=int(height),
                                                 width=int(width),
                                                 sku=sku,
                                                 barcode=barcode,
                                                 inventory=inventory,
                                                 is_deduction_inventory=is_deduction_inventory,
                                                 note=note)
                if type(spec_detail) == str:
                    error_message = "第{row_index}行导入失败，原因：{error_message}" \
                        .format(row_index=row_index, error_message=spec_detail)
                    raise ImportProductsException()
                spec_detail.save()
                # *** END ***

                # *** 创建定价 ***
                if int(row_data[28]) == 1:
                    is_free_shipping = True
                else:
                    is_free_shipping = False
                express_fee_group_id = None
                if is_free_shipping is False:
                    if is_empty(row_data[29]) is False and is_number(row_data[29]) is True and int(row_data[29]) > 0:
                        express_fee_group_id = int(row_data[29])
                    else:
                        error_message = \
                            "第{row_index}行导入失败，原因：第AD列，不包邮产品需要正确的运费模板编码".format(row_index=row_index)
                        raise ImportProductsException()

                currency = str(row_data[19]).upper()

                min_max_numbers = get_min_max_quantity(row_data[20])
                if type(min_max_numbers) == str:
                    error_message = \
                        "第{row_index}行导入失败，原因：{message}".format(row_index=row_index, message=min_max_numbers)
                    raise ImportProductsException()
                else:
                    step_one_min = min_max_numbers[0]
                    step_one_max = min_max_numbers[1]

                if is_number(str(row_data[21]).strip()) is True and float(str(row_data[21]).strip()) > 0:
                    price_one = float(str(row_data[21]).strip())
                else:
                    error_message = \
                        "第{row_index}行导入失败，原因：第V列，价格1数据有误".format(row_index=row_index)
                    raise ImportProductsException()

                min_max_numbers = get_min_max_quantity(row_data[22])
                if type(min_max_numbers) == str:
                    error_message = \
                        "第{row_index}行导入失败，原因：{message}".format(row_index=row_index, message=min_max_numbers)
                    raise ImportProductsException()
                else:
                    step_two_min = min_max_numbers[0]
                    step_two_max = min_max_numbers[1]
                    if is_number(str(row_data[23]).strip()) is True and float(str(row_data[23]).strip()) > 0:
                        price_two = float(str(row_data[23]).strip())
                    elif step_two_min == 0 and step_two_max == 0:
                        price_two = 0
                    else:
                        error_message = \
                            "第{row_index}行导入失败，原因：第X列，价格2数据有误".format(row_index=row_index)
                        raise ImportProductsException()

                min_max_numbers = get_min_max_quantity(row_data[24])
                if type(min_max_numbers) == str:
                    error_message = \
                        "第{row_index}行导入失败，原因：{message}".format(row_index=row_index, message=min_max_numbers)
                    raise ImportProductsException()
                else:
                    step_three_min = min_max_numbers[0]
                    step_three_max = min_max_numbers[1]
                    if is_number(str(row_data[25]).strip()) is True and float(str(row_data[25]).strip()) > 0:
                        price_three = float(str(row_data[25]).strip())
                    elif step_three_min == step_three_max == 0:
                        price_three = 0
                    else:
                        error_message = \
                            "第{row_index}行导入失败，原因：第Z列，价格3数据有误".format(row_index=row_index)
                        raise ImportProductsException()

                retail_price = 0
                suggest_retail_price = 0
                if is_number(str(row_data[26]).strip()) is True and float(str(row_data[26]).strip()) > 0:
                    retail_price = float(str(row_data[26]).strip())
                if is_number(str(row_data[27]).strip()) is True and float(str(row_data[27]).strip()) > 0:
                    suggest_retail_price = float(str(row_data[27]).strip())

                pricing = create_pricing(spec,
                                         is_free_shipping=is_free_shipping,
                                         express_fee_group_id=express_fee_group_id,
                                         currency=currency,
                                         step_one_min=step_one_min,
                                         step_one_max=step_one_max,
                                         price_one=price_one,
                                         step_two_min=step_two_min,
                                         step_two_max=step_two_max,
                                         price_two=price_two,
                                         step_three_min=step_three_min,
                                         step_three_max=step_three_max,
                                         price_three=price_three,
                                         retail_price=retail_price,
                                         suggest_retail_price=suggest_retail_price)
                if type(pricing) == str:
                    error_message = \
                        "第{row_index}行导入失败，原因：{error_message}".format(row_index=row_index, error_message=pricing)
                    raise ImportProductsException()
                # *** END ***

                # *** 创建可售规格关系 ***
                available_spec = create_available_spec(product.creator, spec)
                if type(available_spec) == str:
                    error_message = "第{row_index}行导入失败，原因：{error_message}" \
                        .format(row_index=row_index, error_message=available_spec)
                # *** END ***

                # *** 创建销售方式 ***
                if pricing.wholesale_price > 0 or pricing.has_tiered_pricing:
                    is_wholesale = True
                else:
                    is_wholesale = False

                if pricing.retail_price > 0:
                    is_retail = True
                else:
                    is_retail = False

                product_sales_type = create_product_sales_type(product.creator,
                                                               product,
                                                               is_wholesale=is_wholesale,
                                                               is_retail=is_retail)
                if type(product_sales_type) == str:
                    error_message = "第{row_index}行导入失败，原因：{error_message}" \
                        .format(row_index=row_index, error_message=product_sales_type)
                    raise ImportProductsException()
                product_sales_type.save()
                # *** END ***
                print(str(row_index) + ' - ' + product.name + ' - ' + spec.spec_no)

        except ImportProductsException:
            errors_dict["message" + str(row_index)] = error_message
            print(str(row_index) + ' - ' + error_message)
            time.sleep(0.1)
            continue

        time.sleep(0.1)

    return errors_dict
