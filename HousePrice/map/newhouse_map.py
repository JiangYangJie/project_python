# -*-coding:utf8-*- 
#     create by : JiangYangJie             
#     email     : JiangYangJie@126.com     
#     filename  : newhouse_map   
#     data      : 2019/11/25
import os
from Mysql import mysql
from pyecharts import options as opts
from pyecharts.charts import Map, Page

from map import area,city,county

if not os.path.exists('./html'):
    os.makedirs('./html')
with mysql() as sql:
    info=sql.read("select District,round(AVG(Price),2) from new_house "
               "group by District ORDER BY count(*) DESC limit 28"
               )
Info=[]
for _ in info:
    location = _[0]
    a=""
    if location in area:
        a=location+"区"
    elif location in city:
        a = location+ "市"
    elif location in county:
        a = location+ "县"
    if a!="":
        Info.append([a,_[1]])
c = (
        Map()
        .add("价格", Info, "成都")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="成都区域房价地图"),
            visualmap_opts=opts.VisualMapOpts(max_=20000),
        )
    )
Page.add(c).render(path='./html/newhouse.html')


