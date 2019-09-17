import time

import os

from django.http import HttpResponse

import xlrd
from rest_framework.views import APIView

from apps.logistics.models import Region
from apps.pricing.models import Pricing
from apps.product.models import Category, Product, Spec, Brand, SpecDetail
from .util import Utils


class InitialCategoryView(APIView):
    """
    初始化地区数据
    从.xls导入
    1列:id  2列:pid  3列:name  4列:level  5列:spell  6列:sort
    """
    def get(self, request):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        print(ROOT_DIR)
        file = ROOT_DIR + '\\initial_data\\t_category.xls'
        print(file)
        # """
        wb = xlrd.open_workbook(filename=file)  # 打开文件
        table = wb.sheet_by_index(0)  # 取第一张工作簿
        rows_count = table.nrows  # 取总行数

        for row_index in range(rows_count):  # 行循环

            category = Category()
            row_data = table.row_values(row_index)

            category.id = int(row_data[0])
            if Category.objects.filter(id__exact=int(row_data[0])):
                continue
            category.name = row_data[1]
            category.level = int(row_data[2])
            if row_data[3] is not None and row_data[3] != '' and row_data[3] != 0:
                query_set = Category.objects.filter(id__exact=int(row_data[3]))
                if query_set:
                    category.parent = query_set[0]
                else:
                    category.parent = None
            else:
                category.parent = None

            temp_str = str(category.id) + ' - ' + str(category.name) + ' - '
            if category.parent:
                temp_str += category.parent.name
            else:
                temp_str += 'None'
            print(temp_str)

            category.sort = 0
            category.is_delete = False
            category.is_enable = True
            category.delete_time = None

            category.save()
            time.sleep(0.05)
        # """
        return HttpResponse(request)


class ImportProductsView(APIView):
    """
    批量导入商品数据
    """
    def get(self, request):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        print(ROOT_DIR)
        file = ROOT_DIR + '\\initial_data\\init_product.xls'
        print(file)
        # """
        wb = xlrd.open_workbook(filename=file)  # 打开文件
        table = wb.sheet_by_index(0)  # 取第一张工作簿
        rows_count = table.nrows  # 取总行数

        errors_dict = {}
        for row_index in range(1, rows_count):  # 行循环

            row_data = table.row_values(row_index)

            # 先检测必填项是否填写，如果有一项未填写，直接跳过
            if row_data[0] is None or row_data[0] == '' or row_data[1] is None or row_data[1] == '' or row_data[3] is None or row_data[3] == '' or row_data[8] is None or row_data[8] == '' or row_data[9] is None or row_data[9] == '' or row_data[19] is None or row_data[19] == '' or row_data[24] is None or row_data[24] == '':
                errors_dict["message" + str(row_index)] = "第%row_number行导入失败，原因：第A列为必填项，未填写"
                continue
            if row_data[1] is None or row_data[1] == '':
                errors_dict["message" + str(row_index)] = "第%row_number行导入失败，原因：第B列为必填项，未填写"
                continue
            if row_data[3] is None or row_data[3] == '':
                errors_dict["message" + str(row_index)] = "第%row_number行导入失败，原因：第D列为必填项，未填写"
                continue
            if row_data[8] is None or row_data[8] == '':
                errors_dict["message" + str(row_index)] = "第%row_number行导入失败，原因：第I列为必填项，未填写"
                continue
            if row_data[9] is None or row_data[9] == '':
                errors_dict["message" + str(row_index)] = "第%row_number行导入失败，原因：第J列为必填项，未填写"
                continue
            if row_data[19] is None or row_data[19] == '':
                errors_dict["message" + str(row_index)] = "第%row_number行导入失败，原因：第T列为必填项，未填写"
                continue
            if row_data[24] is None or row_data[24] == '':
                errors_dict["message" + str(row_index)] = "第%row_number行导入失败，原因：第Y列为必填项，未填写"
                continue

            # ***保存商品***
            product = Product()
            product_set = Product.objects.filter(item_no__exact=row_data[3])

            # 如果产品数据库中没有，则创建新产品，如果有，则取出
            if product_set is None:
                product.name = row_data[1]
                product.brief = row_data[2]
                product.item_no = row_data[3]

                # 设定商品分类，如果商品分类未创建，则创建分类
                third_category_set = Category.objects.filter(name__exact=row_data[6])
                if third_category_set:
                    product.category = third_category_set[0]
                else:
                    second_category_set = Category.objects.filter(name__exact=row_data[5])
                    if second_category_set:
                        product.category = Utils.create_category(second_category_set[0], row_data[6])
                    else:
                        first_category_set = Category.objects.filter(name__exact=row_data[4])
                        if first_category_set:
                            second_category = Utils.create_category(first_category_set[0], row_data[5])
                            product.category = Utils.create_category(second_category, row_data[6])
                        else:
                            first_category = Utils.create_category(None, row_data[4])
                            second_category = Utils.create_category(first_category, row_data[5])
                            product.category = Utils.create_category(second_category, row_data[6])

                # 设置商品品牌
                brand_set = Brand.objects.filter(id__extra=int(row_data[7]))
                if brand_set:
                    product.brand = brand_set[0]
                else:
                    product.brand = None

                # 设置商品发货是否需要收件人身份证
                if int(row_data[9]) == 1:
                    product.is_id_needed = True
                else:
                    product.is_id_needed = False

                # 设置原产地和发货地
                product.place_origin = None
                product.place_delivery = Region.objects.filter(name__exact=row_data[8])

                # 设置产品文字描述
                product.desc = row_data[25]

                # 设置商品通用值
                product.sort = 0
                product.is_delete = False
                product.is_enable = True
                product.delete_time = None

                product.save()
            else:
                product = product_set[0]

            # ***保存新规格***
            spec = Spec()
            if row_data[17] is not None and row_data[17] != '':
                spec_set = Spec.objects.filter(spec_no__exact=row_data[17])
                if spec_set:
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

            if int(row_data[25]) == 1:
                spec.is_free_shipping = True
            else:
                spec.is_free_shipping = False
            # todo
            spec.save()

            # 创建规格详情
            spec_detail = SpecDetail()
            spec_detail.spec = spec
            # todo
            spec_detail.save()

            # 创建定价
            pricing = Pricing()
            pricing.spec = spec
            # todo
            pricing.save()

            # 创建阶梯价格，如果有必要
            # todo

            time.sleep(0.05)
        # """
        return HttpResponse(request)