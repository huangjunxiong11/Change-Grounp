# import pandas as pd
#
# df = pd.read_excel('demo.xlsx')
# d = df[['video-name', 'time']].to_dict()
# video_name = d['video-name']
# time_name = d['time']
# for v_key, v_var in video_name.items():
#     for t_key, t_var in time_name.items():
#         if v_key == t_key:
#
#         print(v_key)
#         print(v_var)

# coding=utf-8

import xlrd


class excel_read:
    def __init__(self, excel_path='demo.xlsx', encoding='utf-8', index=0):
        self.data = xlrd.open_workbook(excel_path)  ##获取文本对象
        self.table = self.data.sheets()[index]  ###根据index获取某个sheet
        self.rows = self.table.nrows  ##3获取当前sheet页面的总行数,把每一行数据作为list放到 list

    def get_data(self):
        result = []
        for i in range(self.rows):
            col = self.table.row_values(i)  ##获取每一列数据
            print(col)
            result.append(col)
        # print(result)
        return result


if __name__ == '__main__':
    data = excel_read().get_data()
    # for d in data:
    #     for i in list(d[1]):
    #         print(i)
    #         pass
    import re
    a = '["000000", "000314", "001422", "001814", "002321", "002706", "003115"]'
    b = a.replace("'", "")
    c = list(b)
    print(b)
    pass
