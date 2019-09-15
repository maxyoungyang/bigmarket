import time

import os

from django.http import HttpResponse

import xlrd
from rest_framework.views import APIView

from apps.logistics.models import Region


class InitialRegionView(APIView):
    """
    初始化地区数据
    从.xls导入
    1列:id  2列:pid  3列:name  4列:level  5列:spell  6列:sort
    """
    def get(self, request):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        print(ROOT_DIR)
        file = ROOT_DIR + '\\initial_data\\region.xls'
        print(file)
        # """
        wb = xlrd.open_workbook(filename=file)  # 打开文件
        table = wb.sheet_by_index(0)  # 取第一张工作簿
        rows_count = table.nrows  # 取总行数

        for row_index in range(rows_count):  # 行循环

            region = Region()
            row_data = table.row_values(row_index)

            print(str(row_index) + ' - ' + str(row_data[2]) + ' - ' + str(row_data[3]))

            region.name = row_data[2]
            region.level = int(row_data[3])
            region.spell = ''
            region.sort = 0
            if row_data[1]:
                if Region.objects.filter(id__exact=row_data[1]):
                    region.parent = Region.objects.filter(id__exact=row_data[1])[0]
                else:
                    region.parent = None
            else:
                region.parent = None
            region.is_delete = False
            region.is_enable = True
            region.delete_time = None

            region.save()
            time.sleep(0.05)
        # """
        return HttpResponse(request)
