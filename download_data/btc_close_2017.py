from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from urllib.request import urlopen
from itertools import groupby
import json
import pygal
import math

json_url = 'https://raw.githubusercontent.com/muxuezi/btc/master/btc_close_2017.json'
response = urlopen(json_url)
# 读取数据
req = response.read()
# 将数据写入文件
with open('btc_close_2017_urllib.json', 'wb') as f:
    f.write(req)
# 加载json格式
file_urllib = json.loads(req)
# print(file_urllib)
"""---------------------------"""

# 将数据加载到一个列表中
filename = 'btc_close_2017_urllib.json'
with open(filename) as f:
    btc_data = json.load(f)

# 打印每一天信息
for btc_dict in btc_data:
    date = btc_dict['date']
    month = int(btc_dict['month'])
    week = int(btc_dict['week'])
    weekday = btc_dict['weekday']
    close = int(float(btc_dict['close']))
    # print("{} is month {} week {}, {}, the close price is {} RMB".format(
    #     date, month, week, weekday, close))

# 创建五个列表，分别存储日期和收盘价
dates = []
months = []
weeks = []
weekdays = []
close = []
# 每一天的信息
for btc_dict in btc_data:
    dates.append(btc_dict['date'])
    months.append(int(btc_dict['month']))
    weeks.append(int(btc_dict['week']))
    weekdays.append(btc_dict['weekday'])
    close.append(int(float(btc_dict['close'])))

line_chart = pygal.Line(x_label_rotatioon=20, show_minor_x_labels=False)
line_chart.title = '收盘价 (￥)'
line_chart.x_labels = dates
# X轴坐标每隔二十天显示一次
N = 20
line_chart.x_labels_major = dates[::N]
line_chart.add('收盘价', close)
line_chart.render_to_file('收盘价折线图 (￥).svg')

line_chart = pygal.Line(x_rotation=20, show_minor_x_label=False)
line_chart.title = '收盘价对数变换（￥）'
line_chart.x_labels = dates
# x坐标轴每隔二十天显示一次
N = 20
line_chart.x_labels_major = dates[::N]
close_log = [math.log10(_) for _ in close]
line_chart.add('log收盘价', close_log)
line_chart.render_to_file('收盘价对数变换折线图（￥）.svg')


def draw_line(x_date, y_date, title, y_legend):
    xy_map = []
    for x, y in groupby(sorted(zip(x_date, y_date)), key=lambda _: _[0]):
        y_list = [v for _, v in y]
        xy_map.append([x, sum(y_list) / len(y_list)])
    x_uniqe, y_mean = [*zip(*xy_map)]
    line_chart = pygal.Line()
    line_chart.title = title
    line_chart.x_labels = x_uniqe
    line_chart.add(y_legend, y_mean)
    line_chart.render_to_file(title+'.svg')
    return line_chart


idx_month = dates.index('2017-12-01')
line_chart_month = draw_line(months[:idx_month], close[:idx_month], '收盘价月日均值（￥）', '月日均值')
line_chart_month

idx_week = dates.index('2017-12-01')
line_chart_week = draw_line(months[:idx_month], close[:idx_month], '收盘价周日均值（￥）', '周日均值')
line_chart_week
