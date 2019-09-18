import hashlib
import time

from apps.logistics.models import Region
from apps.pricing.utils import make_pricing
from apps.product.models import Category, Product, Spec, Brand, SpecDetail, ProductSalesType
from apps.user.models import User
from bigmarket.commonutils import get_xls_table, is_empty, is_number


def create_brand(user, name):
    brand = Brand()
    brand.creator = user
    brand.name = name
    brand.save()
    return brand


def create_category(parent_category, name):
    category = Category()
    category.name = name
    category.parent = parent_category
    if parent_category:
        category.level = parent_category.level + 1
    else:
        category.level = 1

    category.sort = 0
    category.is_delete = False
    category.is_enable = True
    category.delete_time = None
    category.save()
    return category


def make_product(creator, name='', brief='', item_no='',
                 first_category_name='', second_category_name='', third_category_name='',
                 brand_name='', place_origin='', place_delivery='',
                 is_id_needed=False, desc=''):
    product = Product()

    # 商品创建人
    if creator is None:
        error_message = "没有指定商品的创建用户"
        return error_message
    else:
        product.creator = creator

    # 商品名称
    if name is None or name == '':
        error_message = "未填写商品名称"
        return error_message
    else:
        product.name = name

    # 商品简述
    product.brief = brief

    # 商品货号
    if item_no is None or item_no == '':
        md5 = hashlib.md5()
        md5.update(name)
        product.item_no = md5.hexdigest()
    else:
        product.item_no = item_no

    # 设定商品分类，如果商品分类未创建，则创建分类，必须一级，二级，三级分类都有数据，否则被归入创建该商品的用户的系统默认分类
    if third_category_name is not None and third_category_name != '':  # 如果输入的商品三级分类名不是空字符串
        third_category_set = Category.objects.filter(name__exact=third_category_name)
        if third_category_set:  # 如果三级分类已存在
            product.category = third_category_set[0]
        else:
            if second_category_name is not None and second_category_name != '':
                second_category_set = Category.objects.filter(name__exact=second_category_name)
                if second_category_set:  # 如果二级分类已存在，则创建新的三级分类，并将产品分类设置为这个新的三级分类
                    product.category = create_category(second_category_set[0], third_category_name)
                else:  # 如果二级分类不存在，则查看一级分类
                    if first_category_name is not None and first_category_name != '':
                        first_category_set = Category.objects.filter(name__exact=first_category_name)
                        if first_category_set:
                            second_category = create_category(first_category_set[0], second_category_name)
                            third_category = create_category(second_category, third_category_name)
                            product.category = third_category
                        else:
                            first_category = create_category(None, first_category_name)
                            second_category = create_category(first_category, second_category_name)
                            third_category = create_category(second_category, third_category_name)
                            product.category = third_category
                    else:
                        error_message = "商品分类必须完整填写三个等级的分类名称，不确定可以不填"
                        return error_message
            else:
                error_message = "商品分类必须完整填写三个等级的分类名称，不确定可以不填"
                return error_message
    else:
        third_category_set = Category.objects.filter(creator=product.creator, name='默认三级', level=3)
        if third_category_set:
            product.category = third_category_set[0]
        else:
            first_default_category = Category()
            first_default_category.creator = product.creator
            first_default_category.level = 1
            first_default_category.name = '默认一级'
            first_default_category.parent = None
            first_default_category.save()
            second_default_category = create_category(first_default_category, '默认二级')
            product.category = create_category(second_default_category, '默认三级')

    if brand_name is not None and brand_name != '':
        brand_set = Brand.objects.filter(name=brand_name)
        if brand_set:
            product.brand = brand_set[0]
        else:
            product.brand = create_brand(creator, brand_name)
    else:
        product.brand = None

    # 设置原产地和发货地
    if Region.objects.filter(name__exact=place_origin):
        product.place_origin = Region.objects.filter(name__exact=place_origin)[0]
    else:
        product.place_origin = None

    if Region.objects.filter(name__exact=place_delivery):
        product.place_delivery = Region.objects.filter(name__exact=place_delivery)[0]
    else:
        product.place_delivery = None

    # 设置商品发货是否需要收件人身份证
    if is_id_needed:
        product.is_id_needed = True
    else:
        product.is_id_needed = False

    # 设置产品文字描述
    product.desc = desc

    product.sort = 0
    product.is_delete = False
    product.is_enable = True
    product.delete_time = None

    return product


def make_spec(product, items=None, spec_no=''):
    spec = Spec()
    spec.product = product

    if items is None or len(items) == 0:
        spec.items = "{\'default\':\'default\'}"
    else:
        spec.items = items

    if spec_no is None or spec_no == '' or Spec.objects.filter(spec_no=spec_no):
        spec_count = Spec.objects.filter(product=product).count()
        spec.spec_no = product.item_no + '-' + str(spec_count + 1)
    else:
        spec.spec_no = spec_no
    return spec


def make_spec_detail(spec,
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
    return spec_detail


def make_product_salse_type(user, product, is_wholesale=True, is_retail=True):
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
    return product_sales_type



def import_multi_products(filepath):
    table = get_xls_table(filepath)
    rows_count = table.nrows  # 取总行数

    errors_dict = {}
    for row_index in range(1, rows_count):  # 行循环

        row_data = table.row_values(row_index)

        # *** 先检测必填项 ***
        if row_data[0] is None or row_data[0] == '' or '.' in str(row_data[0]) or float(row_data[0]) < 1:
            errors_dict["message" + str(row_index)] = \
                "第{row_index}行导入失败，原因：第A列，创建用户ID不正确".format(row_index=row_index)
            continue
        if row_data[1] is None or row_data[1] == '':
            errors_dict["message" + str(row_index)] = \
                "第{row_index}行导入失败，原因：第B列，标题名称为必填项，未填写".format(row_index=row_index)
            continue
        if row_data[8] is None or row_data[8] == '':
            errors_dict["message" + str(row_index)] = \
                "第{row_index}行导入失败，原因：第I列，发货地为必填项，未填写".format(row_index=row_index)
            continue
        if int(row_data[9]) != 0 and int(row_data[9]) != 1:
            errors_dict["message" + str(row_index)] = \
                "第{row_index}行导入失败，原因：第G列，必填且只能填写0或者1,0代表不需要，1代表需要".format(row_index=row_index)
            continue
        if row_data[18].strip().upper() not in 'CNY CNH CAD USD AUD NZD EUR JPY GBP HKD KRW':
            errors_dict["message" + str(row_index)] = \
                "第{row_index}行导入失败，原因：第S列，商品计价币种填写错误".format(row_index=row_index)

        if is_number(row_data[20]) is False:
            errors_dict["message" + str(row_index)] = \
                "第{row_index}行导入失败，原因：第U列，至少需要设置一个正确价格".format(row_index=row_index)
            continue

        if float(row_data[27]) != 0 and float(row_data[27]) != 1:
            errors_dict["message" + str(row_index)] = \
                "第{row_index}行导入失败，原因：第AB列，只能填写0或者1,0代表不包邮，1代表包邮".format(row_index=row_index)
            continue

        if float(row_data[41]) != 0 and float(row_data[41]) != 1:
            errors_dict["message" + str(row_index)] = \
                "第{row_index}行导入失败，原因：第AP列，只能填写0或者1,0代表不供货，1代表供货（代发批发）".format(row_index=row_index)
            continue
        if float(row_data[42]) != 0 and float(row_data[42]) != 1:
            errors_dict["message" + str(row_index)] = \
                "第{row_index}行导入失败，原因：第AQ列，只能填写0或者1,0代表不零售，1代表零售".format(row_index=row_index)
            continue

        if float(row_data[41]) == 0 and float(row_data[42]) == 0:
            errors_dict["message" + str(row_index)] = \
                "第{row_index}行导入失败，原因：第AP,AQ列，不能同时为0".format(row_index=row_index)
            continue

        if float(row_data[42]) == 0:
            if is_number(row_data[26]) is False or float(row_data[26]) <= 0:
                errors_dict["message" + str(row_index)] = \
                    "第{row_index}行导入失败，原因：第AA列，设置零售的商品，必须填写正确的零售价格".format(row_index=row_index)
                continue
        # *** END ***

        # *** 创建商品对象 ***
        # 根据商品货号进行查找，如果该商品已存在，则从数据库中取出，如果不存在则创建新商品
        product_set = Product.objects.filter(item_no__exact=row_data[3])
        if product_set is None:
            # 获得创建商品用户
            creator = None
            user_set = User.objects.filter(id__extra=row_data[0])
            if user_set:
                creator = user_set[0]
            else:
                errors_dict["message" + str(row_index)] = \
                    "第{row_index}行导入失败，原因：第A列，创建用户ID不正确".format(row_index=row_index)
                continue
            # 获得商品简述
            name = row_data[1]
            brief = row_data[2]
            item_no = row_data[3]
            first_category_name = row_data[4]
            second_category_name = row_data[5]
            third_category_name = row_data[6]
            brand_name = row_data[7]
            place_delivery = row_data[8]
            is_id_needed = False
            if int(row_data[9]) == 1:
                is_id_needed = True

            desc = row_data[40]
            product = make_product(creator,
                                   name=name,
                                   brief=brief,
                                   item_no=item_no,
                                   first_category_name=first_category_name,
                                   second_category_name=second_category_name,
                                   third_category_name=third_category_name,
                                   brand_name=brand_name,
                                   place_delivery=place_delivery,
                                   is_id_needed=is_id_needed,
                                   desc=desc)
            if type(product) == str:
                errors_dict["message" + str(row_index)] = \
                    "第{row_index}行导入失败，原因：{error_message}".format(row_index=row_index, error_message=product)
                continue
        else:
            product = product_set[0]

        # ***保存新规格***
        items = {}
        if row_data[12] == '' and row_data[13] == '' and row_data[14] == '' and row_data[15] == '' and row_data[
            16] == '' and row_data[17] == '':
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
        if Spec.objects.filter(spec_no=spec_no):
            errors_dict["message" + str(row_index)] = \
                "第{row_index}行导入失败，原因：第S列，规格编码重复，请修正".format(row_index=row_index)
            continue

        spec = make_spec(product, items, spec_no)
        if type(spec) == str:
            errors_dict["message" + str(row_index)] = \
                "第{row_index}行导入失败，原因：{error_message}".format(row_index=row_index, error_message=spec)
            continue

        # 创建规格详情
        if row_data[10] is not None and row_data[10] != '':
            if is_number(row_data[10]):
                min_order_quantity = int(row_data[10])
            else:
                errors_dict["message" + str(row_index)] = \
                    "第{row_index}行导入失败，原因：第K列，最小起订量必须是正整数".format(row_index=row_index)
                continue
        else:
            min_order_quantity = 1

        if row_data[11] is not None and row_data[11] != '':
            if is_number(row_data[11]):
                max_order_quantity = int(row_data[11])
                if max_order_quantity < min_order_quantity:
                    errors_dict["message" + str(row_index)] = \
                        "第{row_index}行导入失败，原因：第L列，最大订购量必须是正整数".format(row_index=row_index)
                    continue
            else:
                errors_dict["message" + str(row_index)] = \
                    "第{row_index}行导入失败，原因：第L列，最大订购量必须大于等于最小起订量".format(row_index=row_index)
                continue
        else:
            max_order_quantity = 9999

        note = row_data[38]

        if (is_empty(row_data[30]) is False and is_number(row_data[30]) is False) or (
                is_number(row_data[30]) is True and float(row_data[30]) <= 0):
            errors_dict["message" + str(row_index)] = \
                "第{row_index}行导入失败，原因：第AE列，毛重必须为数字，且大于0，非必填".format(row_index=row_index)
            continue
        gross_weight = float(row_data[30])

        if (is_empty(row_data[31]) is False and is_number(row_data[31]) is False) or (
                is_number(row_data[31]) is True and float(row_data[31]) <= 0):
            errors_dict["message" + str(row_index)] = \
                "第{row_index}行导入失败，原因：第AF列，长必须为数字，且大于0，非必填".format(row_index=row_index)
            continue
        length = float(row_data[31])

        if (is_empty(row_data[32]) is False and is_number(row_data[32]) is False) or (
                is_number(row_data[32]) is True and float(row_data[32]) <= 0):
            errors_dict["message" + str(row_index)] = \
                "第{row_index}行导入失败，原因：第AG列，宽度必须为数字，且大于0，非必填".format(row_index=row_index)
            continue
        width = float(row_data[32])

        if (is_empty(row_data[33]) is False and is_number(row_data[33]) is False) or (
                is_number(row_data[33]) is True and float(row_data[33]) <= 0):
            errors_dict["message" + str(row_index)] = \
                "第{row_index}行导入失败，原因：第AH列，高度必须为数字，且大于0，非必填".format(row_index=row_index)
            continue
        height = float(row_data[33])

        sku = row_data[34]
        barcode = row_data[35]

        if is_empty(row_data[36]) is False and is_number(row_data[36]) is True and int(row_data[36]) >= 0:
            inventory = int(row_data[36])
            is_deduction_inventory = True
        else:
            inventory = 9999
            is_deduction_inventory = False

        spec_detail = make_spec_detail(spec,
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
            errors_dict["message" + str(row_index)] = \
                "第{row_index}行导入失败，原因：{error_message}".format(row_index=row_index, error_message=spec_detail)
            continue
        # 创建定价
        if int(row_data[28]) == 1:
            is_free_shipping = True
        else:
            is_free_shipping = False
        express_fee_group_id = None
        if is_free_shipping is False:
            if is_empty(row_data[29]) is False and is_number(row_data[29]) is True and int(row_data[29]) > 0:
                express_fee_group_id = int(row_data[29])
            else:
                errors_dict["message" + str(row_index)] = \
                    "第{row_index}行导入失败，原因：第AD列，不包邮产品需要正确的运费模板编码".format(row_index=row_index)
                continue

        currency = str(row_data[19]).upper()

        step_one_min = 0
        step_one_max = 0
        if is_empty(row_data[20]) is False:
            min_max_list = str(row_data[20]).split('-')
            if len(min_max_list) == 2 and is_number(min_max_list[0].strip()) is True and is_number(
                    min_max_list[1].strip()) is True and int(min_max_list[1]) > int(min_max_list[0]):
                step_one_min = int(min_max_list[0])
                step_one_max = int(min_max_list[1])

        if is_number(row_data[21].strip()) is True and float(row_data[21].strip() > 0):
            price_one = float(row_data[21].strip())
        else:
            errors_dict["message" + str(row_index)] = \
                "第{row_index}行导入失败，原因：第V列，价格1数据有误".format(row_index=row_index)
            continue

        step_two_min = 0
        step_two_max = 0
        price_two = 0
        if is_empty(row_data[22]) is False:
            min_max_list = str(row_data[22]).split('-')
            if len(min_max_list) == 2 and is_number(min_max_list[0].strip()) is True and is_number(
                    min_max_list[1].strip()) is True and int(min_max_list[1]) > int(min_max_list[0]):
                step_two_min = int(min_max_list[0])
                step_two_max = int(min_max_list[1])
                if is_number(row_data[23].strip()) is True and float(row_data[23].strip() > 0):
                    price_two = float(row_data[23].strip())
                else:
                    errors_dict["message" + str(row_index)] = \
                        "第{row_index}行导入失败，原因：第X列，价格2数据有误".format(row_index=row_index)
                    continue

        step_three_min = 0
        step_three_max = 0
        price_three = 0
        if is_empty(row_data[24]) is False:
            min_max_list = str(row_data[24]).split('-')
            if len(min_max_list) == 2 and is_number(min_max_list[0].strip()) is True and is_number(
                    min_max_list[1].strip()) is True and int(min_max_list[1]) > int(min_max_list[0]):
                step_three_min = int(min_max_list[0])
                step_three_max = int(min_max_list[1])
                if is_number(row_data[25].strip()) is True and float(row_data[25].strip() > 0):
                    price_three = float(row_data[25].strip())
                else:
                    errors_dict["message" + str(row_index)] = \
                        "第{row_index}行导入失败，原因：第Z列，价格3数据有误".format(row_index=row_index)
                    continue

        retail_price = 0
        suggest_retail_price = 0
        if is_number(row_data[26].strip()) is True and float(row_data[26].strip() > 0):
            retail_price = float(row_data[26].strip())
        if is_number(row_data[27].strip()) is True and float(row_data[27].strip() > 0):
            suggest_retail_price = float(row_data[27].strip())

        pricing = make_pricing(spec,
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
            errors_dict["message" + str(row_index)] = \
                "第{row_index}行导入失败，原因：{error_message}".format(row_index=row_index, error_message=pricing)
            continue

        # 创建销售方式
        is_wholesale = True if int(row_data[41]) == 1 else False
        is_retail = True if int(row_data[42]) == 1 else False

        product_sales_type = make_product_salse_type(product.creator,
                                                     product,
                                                     is_wholesale=is_wholesale,
                                                     is_retail=is_retail)
        if type(product_sales_type) == str:
            errors_dict["message" + str(row_index)] = \
                "第{row_index}行导入失败，原因：{error_message}".format(row_index=row_index, error_message=product_sales_type)
            continue

        product.save()
        spec.save()
        spec_detail.save()
        pricing.save()
        if pricing.has_tiered_pricing is True:
            pricing.tiered_pricing.save()
            for step_price in pricing.tiered_pricing.step_price:
                step_price.save()
        product_sales_type.save()

        time.sleep(0.05)
