import os
import xlrd


def get_xls_table(filepath):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    print(ROOT_DIR)
    file = ROOT_DIR + filepath
    print(file)
    # """
    wb = xlrd.open_workbook(filename=file)  # 打开文件
    table = wb.sheet_by_index(0)  # 取第一张工作簿
    return table