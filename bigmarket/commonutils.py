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

def content_is_number(content):
    if content is None or content != '':
        return False
    else:
        try:
            float(content)
            return True
        except ValueError:
            return False

def cell_has_content(cell_content):
    if cell_content is not None and cell_content != '':
        return True
    else:
        return False
