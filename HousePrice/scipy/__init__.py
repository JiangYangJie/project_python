# -*-coding:utf8-*- 
#     create by : JiangYangJie             
#     email     : JiangYangJie@126.com     
#     filename  : __init__.py   
#     data      : 2019/11/18                      
from . scipy import NewHouse,Second_Hand_Scipy,ScipyThread,RentHouse


# u = 'https://cd.fang.lianjia.com/loupan/nhs2pg{}/'
# u = 'https://cd.lianjia.com/ershoufang/pg{}/'
# u = 'https://cd.lianjia.com/ershoufang/pg{}co32/'
# u = 'https://cd.lianjia.com/zufang/pg{}/#contentList'
# u = 'https://cd.lianjia.com/zufang/pg{}rco11/#contentList'
def NewHouseScipy(url,start=1,end=100):
    l=[ ScipyThread(str(i),NewHouse(url.format(i),i)) for i in range(start,end) ]
    for _ in l:
        _.start()
    for _ in l:
        _.join()

def SecondHandScipy(url,start=1,end=100):
    l=[ ScipyThread(str(i),Second_Hand_Scipy(url.format(i),i)) for i in range(start,end) ]
    for _ in l:
        _.start()
    for _ in l:
        _.join()

def RentHouseScipy(url,start=1,end=100):
    l=[ ScipyThread(str(i),RentHouse(url.format(i),i)) for i in range(start,end) ]
    for _ in l:
        _.start()
    for _ in l:
        _.join()



