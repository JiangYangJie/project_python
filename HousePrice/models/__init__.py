# -*-coding:utf8-*- 
#     create by : JiangYangJie             
#     email     : JiangYangJie@126.com     
#     filename  : __init__.py   
#     data      : 2019/11/18
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from .models import second_hand

engine=create_engine('mysql+mysqlconnector://root:admin@127.0.0.1:3306/HousePrice?charset=utf8mb4')
Base = declarative_base()
