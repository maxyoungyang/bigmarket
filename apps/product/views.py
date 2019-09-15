import time

import os

from django.http import HttpResponse

import xlrd
from rest_framework.views import APIView

from apps.logistics.models import Region
from apps.product.models import Category


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

            print(str(row_index) + ' - ' + str(row_data[0]) + ' - ' + str(row_data[1]))

            category.id = int(row_data[0])
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
            category.sort = 0
            category.is_delete = False
            category.is_enable = True
            category.delete_time = None

            category.save()
            time.sleep(0.05)
        # """
        return HttpResponse(request)
