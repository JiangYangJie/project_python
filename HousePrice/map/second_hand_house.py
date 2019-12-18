# -*-coding:utf8-*- 
#     create by : JiangYangJie             
#     email     : JiangYangJie@126.com     
#     filename  : second_hand_house   
#     data      : 2019/11/25
import os
from Mysql import mysql
from pyecharts import options as opts
from pyecharts.charts import Map, Page, Pie

if not os.path.exists('./html'):
    os.makedirs('./html')
def Renovation():
    with mysql() as sql:
        info=sql.read("select Renovation,count(*) from second_hand "
                      "group by Renovation ORDER BY count(*) DESC limit 30"
               )
    Sum = sum([_[1] for _ in info])
    ave = [100*_[1]/Sum for _ in info]
    Info = [_[0] for _ in info]
    c = (
        Pie()
            .add("", [list(z) for z in zip(Info,ave)])
            .set_colors(["blue", "green", "red", "pink", "orange", "purple"])
            .set_global_opts(title_opts=opts.TitleOpts(title="成都二手房装修情况"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    Page.add(c).render(path='./html/renovation_second.html')
Renovation()











