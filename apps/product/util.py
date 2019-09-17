import time

from apps.logistics.models import Region
from apps.pricing.models import Pricing, TieredPricing, StepPrice
from apps.product.models import Category, Product, Spec, Brand, SpecDetail
from apps.logistics.models import ExpressFeeGroup
from apps.user.models import User, AgentGroup
from bigmarket.commonutils import get_xls_table, content_is_number, cell_has_content


class Utils:

    @staticmethod
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

    @staticmethod
    def import_multi_products(filepath):
        table = get_xls_table(filepath)
        rows_count = table.nrows  # 取总行数

        errors_dict = {}
        for row_index in range(1, rows_count):  # 行循环

            row_data = table.row_values(row_index)

            # 先检测必填项是否填写，如果有一项未填写，直接跳过
            if row_data[0] is None or row_data[0] == '':
                errors_dict["message" + str(row_index)] = \
                    "第{row_index}行导入失败，原因：第A列，创建用户ID为必填项，未填写".format(row_index=row_index)
                continue
            if row_data[1] is None or row_data[1] == '':
                errors_dict["message" + str(row_index)] = \
                    "第{row_index}行导入失败，原因：第B列，标题名称为必填项，未填写".format(row_index=row_index)
                continue
            if row_data[3] is None or row_data[3] == '':
                errors_dict["message" + str(row_index)] = \
                    "第{row_index}行导入失败，原因：第D列，货号为必填项，未填写".format(row_index=row_index)
                continue
            if row_data[8] is None or row_data[8] == '':
                errors_dict["message" + str(row_index)] = \
                    "第{row_index}行导入失败，原因：第I列，发货地为必填项，未填写".format(row_index=row_index)
                continue
            if row_data[9] != 0 and row_data[9] != 1:
                errors_dict["message" + str(row_index)] = \
                    "第{row_index}行导入失败，原因：第G列，必填且只能填写0或者1,0代表不需要，1代表需要".format(row_index=row_index)
                continue
            if row_data[18].strip().upper() not in 'CNY CNH CAD USD AUD NZD EUR JPY GBP HKD KRW':
                errors_dict["message" + str(row_index)] = \
                    "第{row_index}行导入失败，原因：第S列，商品计价币种填写错误".format(row_index=row_index)

            if content_is_number(row_data[20]) is False:
                errors_dict["message" + str(row_index)] = \
                    "第{row_index}行导入失败，原因：第U列，至少需要设置一个正确价格".format(row_index=row_index)
                continue

            if row_data[27] != 0 and row_data[27] != 1:
                errors_dict["message" + str(row_index)] = \
                    "第{row_index}行导入失败，原因：第AB列，只能填写0或者1,0代表不包邮，1代表包邮".format(row_index=row_index)
                continue

            # ***保存商品***
            product = Product()
            product_set = Product.objects.filter(item_no__exact=row_data[3])

            # 如果产品数据库中没有，则创建新产品，如果有，则取出
            if product_set is None:
                creator_set = User.objects.filter(id__extra=int(row_data[0]))
                if creator_set:
                    product.creator = creator_set[0]
                else:
                    errors_dict["message" + str(row_index)] = \
                        "第{row_index}行导入失败，原因：第A列，创建人ID有误".format(row_index=row_index)
                    continue
                product.name = row_data[1]
                product.brief = row_data[2]
                product.item_no = row_data[3]

                if (row_data[4] is None or row_data[4] == '') and (row_data[5] is None or row_data[5] == '') and (row_data[6] is None or row_data[6] == ''):
                    errors_dict["message" + str(row_index)] = \
                        "第{row_index}行导入失败，原因：第EFG三列，至少要为商品指定一个分类".format(row_index=row_index)
                    continue

                # 设定商品分类，如果商品分类未创建，则创建分类
                third_category_set = Category.objects.filter(name__exact=row_data[6])
                if third_category_set:
                    product.category = third_category_set[0]
                else:
                    second_category_set = Category.objects.filter(name__exact=row_data[5])
                    if second_category_set:
                        if row_data[6] != '' and row_data[6] is not None:
                            product.category = Utils.create_category(second_category_set[0], row_data[6])
                        else:
                            product.category = second_category_set[0]
                    else:
                        first_category_set = Category.objects.filter(name__exact=row_data[4])
                        if first_category_set:
                            if row_data[5] != '' and row_data[5] is not None:
                                second_category = Utils.create_category(first_category_set[0], row_data[5])
                                if row_data[6] != '' and row_data[6] is not None:
                                    product.category = Utils.create_category(second_category, row_data[6])
                                else:
                                    product.category = second_category
                            else:
                                product.category = first_category_set[0]
                        else:
                            first_category = Utils.create_category(None, row_data[4])
                            if row_data[5] != '' and row_data[5] is not None:
                                second_category = Utils.create_category(first_category, row_data[5])
                                if row_data[6] != '' and row_data[6] is not None:
                                    product.category = Utils.create_category(second_category, row_data[6])
                                else:
                                    product.category = second_category
                            else:
                                product.category = first_category

                # 设置商品品牌
                if (row_data[7]is not None and row_data[7] != '') and (content_is_number(row_data[7]) is False or int(row_data[7]) <= 0):
                    errors_dict["message" + str(row_index)] = \
                        "第{row_index}行导入失败，原因：第H三列，品牌ID必须是大于0的整数或者不填".format(row_index=row_index)
                    continue
                brand_set = Brand.objects.filter(id__extra=int(row_data[7]))
                if brand_set:
                    product.brand = brand_set[0]
                else:
                    product.brand = None

                # 设置原产地和发货地
                product.place_origin = None
                if Region.objects.filter(name__exact=row_data[8]):
                    product.place_delivery = Region.objects.filter(name__exact=row_data[8])[0]
                else:
                    product.place_delivery = None

                # 设置商品发货是否需要收件人身份证
                if int(row_data[9]) == 1:
                    product.is_id_needed = True
                else:
                    product.is_id_needed = False

                # 设置产品文字描述
                product.desc = row_data[38]

                # 设置商品通用值
                product.sort = 0
                product.is_delete = False
                product.is_enable = True
                product.delete_time = None
            else:
                product = product_set[0]

            # ***保存新规格***
            spec = Spec()
            if row_data[17] is not None and row_data[17] != '':
                spec_set = Spec.objects.filter(spec_no__exact=row_data[17])
                if spec_set:
                    errors_dict["message" + str(row_index)] = \
                        "第{row_index}行导入失败，原因：第R列，规格编码不能重复，可以使用条形码，SKU编码作为规格编码".format(row_index=row_index)
                    continue
                else:
                    spec.product = product
                    spec.name = row_data[11] + ',' + row_data[13] + ',' + row_data[15]
                    spec.value = row_data[12] + ',' + row_data[14] + ',' + row_data[16]
                    spec.spec_no = row_data[17]
            else:
                spec.product = product
                spec.name = 'default'
                spec.value = 'default'
                spec.spec_no = 'default'

            # 创建规格详情
            spec_detail = SpecDetail()
            spec_detail.spec = spec
            spec_detail.note = row_data[36]

            if cell_has_content(row_data[29]) and (content_is_number(row_data[29]) is False or float(row_data[29]) <= 0):
                errors_dict["message" + str(row_index)] = \
                    "第{row_index}行导入失败，原因：第AD列，毛重必须为数字，且大于0或者不填".format(row_index=row_index)
                continue
            spec_detail.gross_weight = row_data[29]

            if cell_has_content(row_data[30]) and (content_is_number(row_data[30]) is False or float(row_data[30]) <= 0):
                errors_dict["message" + str(row_index)] = \
                    "第{row_index}行导入失败，原因：第AE列，长度必须为数字，且大于0或者不填".format(row_index=row_index)
                continue
            spec_detail.length = row_data[30]

            if cell_has_content(row_data[31]) and (content_is_number(row_data[31]) is False or float(row_data[31]) <= 0):
                errors_dict["message" + str(row_index)] = \
                    "第{row_index}行导入失败，原因：第AF列，宽度必须为数字，且大于0或者不填".format(row_index=row_index)
                continue
            spec_detail.width = row_data[31]

            if cell_has_content(row_data[32]) and (content_is_number(row_data[32]) is False or float(row_data[32]) <= 0):
                errors_dict["message" + str(row_index)] = \
                    "第{row_index}行导入失败，原因：第AG列，高度必须为数字，且大于0或者不填".format(row_index=row_index)
                continue
            spec_detail.height = row_data[32]

            spec_detail.sku = row_data[33]

            if content_is_number(row_data[34]) is False:
                errors_dict["message" + str(row_index)] = \
                    "第{row_index}行导入失败，原因：第AI列，条码必须为数字或者不填".format(row_index=row_index)
                continue
            spec_detail.barcode = row_data[34]

            if cell_has_content(row_data[35]) and content_is_number(row_data[35]) and float(row_data[35]) >= 0:
                spec_detail.inventory = int(row_data[35])
                spec_detail.is_deduction_inventory = True
            else:
                spec_detail.inventory = 9999
                spec_detail.is_deduction_inventory = False

            if row_data[10] and row_data[10] != '':
                limit_quantity_set = row_data[10].split('-')
                if len(limit_quantity_set) == 2:
                    if content_is_number(limit_quantity_set[0]) and content_is_number(limit_quantity_set[1]):
                        spec_detail.min_quantity = int(limit_quantity_set[0].strip())
                        spec_detail.max_quantity = int(limit_quantity_set[1].strip())
                    else:
                        spec_detail.min_quantity = 1
                        spec_detail.max_quantity = 999
                else:
                    spec_detail.min_quantity = 1
                    spec_detail.max_quantity = 999
            else:
                spec_detail.min_quantity = 1
                spec_detail.max_quantity = 999

            # ***创建该规格的定价***
            pricing = Pricing()
            pricing.spec = spec
            # 该定价是否包邮
            if int(row_data[27]) == 1:
                pricing.is_free_shipping = True
            else:
                pricing.is_free_shipping = False
                express_fee_group_set = ExpressFeeGroup.objects.filter(id__extra=int(row_data[28]))
                if express_fee_group_set:
                    pricing.express_fee_group = express_fee_group_set[0]
                else:
                    errors_dict["message" + str(row_index)] = \
                        "第{row_index}行导入失败，原因：第AC列，设置为不包邮却未指定快递费模板ID".format(row_index=row_index)
                    continue

            pricing.currency = row_data[18].upper()
            pricing.cost = 0

            if cell_has_content(row_data[20]) and content_is_number(row_data[20]) and float(row_data[20]) >= 0:
                if row_data[19] is None or row_data[19] == '':
                    pricing.wholesale_price = float(row_data[20])
                    pricing.has_tiered_pricing = False
                else:
                    pricing.wholesale_price = 0
                    pricing.has_tiered_pricing = True
            else:
                errors_dict["message" + str(row_index)] = \
                    "第{row_index}行导入失败，原因：第U列，价格1必须为大于零的数字".format(row_index=row_index)
                continue

            if cell_has_content(row_data[25]) and content_is_number(row_data[25]) and float(row_data[25]) >= 0:
                pricing.retail_price = float(row_data[25])
            else:
                errors_dict["message" + str(row_index)] = \
                    "第{row_index}行导入失败，原因：第Z列，零售价必须为数字或者不填".format(row_index=row_index)
                continue

            if cell_has_content(row_data[26]) and content_is_number(row_data[26]) and float(row_data[26]) >= 0:
                pricing.suggested_retail_price = float(row_data[26])
            else:
                errors_dict["message" + str(row_index)] = \
                    "第{row_index}行导入失败，原因：第AA列，市场价必须为数字或者不填".format(row_index=row_index)
                continue

            pricing.is_general = True

            if product.creator:
                agent_group_set = AgentGroup.objects.filter(supplier__extra=product.creator, name__exact='默认')
                if agent_group_set:
                    pricing.agent_group = agent_group_set[0]
                else:
                    default_agent_group = AgentGroup()
                    default_agent_group.supplier = product.creator
                    default_agent_group.name = '默认'
                    default_agent_group.desc = '默认代理分组'
                    pricing.agent_group = default_agent_group
                    default_agent_group.save()

            # 创建阶梯价格，如果有必要
            tiered_pricing = None
            if pricing.has_tiered_pricing is True:
                tiered_pricing = TieredPricing()
                tiered_pricing.price = pricing
                # 创建阶梯价格的各级阶梯
                step_price_list = []
                if cell_has_content(row_data[19]):
                    step_price = StepPrice()
                    limit_quantity_set = row_data[19].split('-')
                    if len(limit_quantity_set) == 2:
                        if content_is_number(limit_quantity_set[0]) and content_is_number(limit_quantity_set[1]):
                            step_price.min_quantity = int(limit_quantity_set[0].strip())
                            step_price.max_quantity = int(limit_quantity_set[1].strip())
                            step_price.tiered_pricing = tiered_pricing
                            if cell_has_content(row_data[20]) and content_is_number(row_data[20]) and float(
                                    row_data[20]) >= 0:
                                step_price.price = float(row_data[20])
                            else:
                                errors_dict["message" + str(row_index)] = \
                                    "第{row_index}行导入失败，原因：第U列，价格必须为大于0的数字".format(row_index=row_index)
                                continue
                            step_price_list.append(step_price)
                        else:
                            errors_dict["message" + str(row_index)] = \
                                "第{row_index}行导入失败，原因：第T列，阶梯数量设置有误".format(row_index=row_index)
                            continue
                    else:
                        errors_dict["message" + str(row_index)] = \
                            "第{row_index}行导入失败，原因：第T列，阶梯数量设置有误".format(row_index=row_index)
                        continue

                if cell_has_content(row_data[21]):
                    step_price = StepPrice()
                    limit_quantity_set = row_data[21].split('-')
                    if len(limit_quantity_set) == 2:
                        if content_is_number(limit_quantity_set[0]) and content_is_number(limit_quantity_set[1]):
                            step_price.min_quantity = int(limit_quantity_set[0].strip())
                            step_price.max_quantity = int(limit_quantity_set[1].strip())
                            step_price.tiered_pricing = tiered_pricing
                            if cell_has_content(row_data[22]) and content_is_number(row_data[22]) and float(
                                    row_data[22]) >= 0:
                                step_price.price = float(row_data[22])
                            else:
                                errors_dict["message" + str(row_index)] = \
                                    "第{row_index}行导入失败，原因：第W列，价格必须为大于0的数字".format(row_index=row_index)
                                continue
                            step_price_list.append(step_price)
                        else:
                            errors_dict["message" + str(row_index)] = \
                                "第{row_index}行导入失败，原因：第V列，阶梯数量设置有误".format(row_index=row_index)
                            continue
                    else:
                        errors_dict["message" + str(row_index)] = \
                            "第{row_index}行导入失败，原因：第V列，阶梯数量设置有误".format(row_index=row_index)
                        continue

                if cell_has_content(row_data[23]):
                    step_price = StepPrice()
                    limit_quantity_set = row_data[23].split('-')
                    if len(limit_quantity_set) == 2:
                        if content_is_number(limit_quantity_set[0]) and content_is_number(limit_quantity_set[1]):
                            step_price.min_quantity = int(limit_quantity_set[0].strip())
                            step_price.max_quantity = int(limit_quantity_set[1].strip())
                            step_price.tiered_pricing = tiered_pricing
                            if cell_has_content(row_data[24]) and content_is_number(row_data[24]) and float(
                                    row_data[24]) >= 0:
                                step_price.price = float(row_data[24])
                            else:
                                errors_dict["message" + str(row_index)] = \
                                    "第{row_index}行导入失败，原因：第Y列，价格必须为大于0的数字".format(row_index=row_index)
                                continue
                            step_price_list.append(step_price)
                        else:
                            errors_dict["message" + str(row_index)] = \
                                "第{row_index}行导入失败，原因：第X列，阶梯数量设置有误".format(row_index=row_index)
                            continue
                    else:
                        errors_dict["message" + str(row_index)] = \
                            "第{row_index}行导入失败，原因：第X列，阶梯数量设置有误".format(row_index=row_index)
                        continue

                if len(step_price_list) == 0:
                    errors_dict["message" + str(row_index)] = \
                        "第{row_index}行导入失败，原因：阶梯价格设置有误，请检查".format(row_index=row_index)
                    continue

            product.save()
            spec.save()
            spec_detail.save()
            pricing.save()

            if tiered_pricing is not False:
                tiered_pricing.save()
                if step_price_list is not None and len(step_price_list) > 0:
                    for step_price in step_price_list:
                        step_price.save()

            time.sleep(0.05)