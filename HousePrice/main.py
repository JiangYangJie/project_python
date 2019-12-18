# -*-coding:utf8-*- 
#     create by : JiangYangJie             
#     email     : JiangYangJie@126.com     
#     filename  : main   
#     data      : 2019/11/19
import time

from scipy import NewHouseScipy, ScipyThread, Second_Hand_Scipy,RentHouse

now = time.time()
NewHouseScipy('https://cd.fang.lianjia.com/loupan/nhs2pg{}/',1,5)
print(time.time()-now)