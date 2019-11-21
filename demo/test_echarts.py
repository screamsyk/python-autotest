import json

from pyecharts import options as opts
from pyecharts.faker import Faker
from pyecharts.charts import Line
from pyecharts.globals import ThemeType


def main():
    with open('result2.json') as f:
        result = json.load(f)
        xaxis = []
        yaxis_cpu_percent = []
        yaxis_memory_percent = []
        for item in result['records']:
            xaxis.append(item['time'])
            yaxis_cpu_percent.append(item['cpu_percent'])
            yaxis_memory_percent.append(item['memory_percent'])
        line = (
            Line(
                init_opts={
                    'theme': ThemeType.LIGHT,
                    'width': '1400px',
                    'height': '600px',
                    'page_title': result['title']
                }
            )
            .add_xaxis(xaxis)
            .add_yaxis('CPU 使用率', yaxis_cpu_percent, markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]))
            .add_yaxis('内存使用率', yaxis_memory_percent, markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]))
            .set_global_opts(
                title_opts={
                    'text': result['title'],
                    'pos_left': 'center'
                },
                datazoom_opts={
                    'is_show': True
                },
                tooltip_opts={
                    'trigger': 'axis'
                },
                xaxis_opts={
                    'name': '时间'
                },
                yaxis_opts={
                    'name': '百分比',
                    'max': 100
                }
            )
        )
        line.render(result['title']+'.html')


if __name__ == '__main__':
    main()
