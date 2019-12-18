# -*-coding:utf8-*- 
#     create by : JiangYangJie             
#     email     : JiangYangJie@126.com     
#     filename  : rent_house_map   
#     data      : 2019/11/25
import os
from Mysql import mysql
from pyecharts import options as opts
from pyecharts.charts import Bar, Page

with mysql() as sql:
    info=sql.read("select District,count(*) from rent_house "
                  "group by District ORDER BY count(*) DESC limit 19")
x=[ _[0] for _ in info]
y=[ _[1] for _ in info]

c=(
    Bar().add_xaxis(x)
    .add_yaxis('总计',y)
    .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
)
Page().add(c).render('./html/rent_district.html')