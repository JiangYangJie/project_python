# -*-coding:utf8-*- 
#     create by : JiangYangJie             
#     email     : JiangYangJie@126.com     
#     filename  : models   
#     data      : 2019/11/18



from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime, func, Float, Date
from sqlalchemy.ext.declarative import declarative_base
# from .__init__ import Base
from sqlalchemy.orm import sessionmaker

engine=create_engine('mysql+mysqlconnector://root:admin@127.0.0.1:3306/HousePrice?charset=utf8mb4')
Base = declarative_base()

class CellInformation(Base):  #小区信息
    __tablename__ = 'Cell_information'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    id = Column(Integer,nullable=False,autoincrement=True,primary_key=True)
    lat = Column(Float,nullable=False,comment='经度')
    lng = Column(Float,nullable=False,comment='纬度')
    address = Column(String(100),nullable=False,comment='具体地址')
    province =Column(String(10),nullable=False,comment='省')
    city =Column(String(10),nullable=False,comment='城市')
    area = Column(String(10),nullable=False,comment='区')


class second_hand(Base):
    __tablename__ = 'second_hand'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    # Title,Cellname,Location,Totalprice,UnitPrice,Apartment,Area,Orientation,Renovation,Floor,Construction_time,Characteristics_apartment,Follow,Release_time
    Title = Column(String(64), primary_key=True,comment='帖子名字')  #帖子名字
    Cellname = Column(String(50),nullable=False,comment='小区名字')    #小区名字
    Location = Column(String(50),default='None',comment='位置')   #位置
    Totalprice = Column(Float,default=0,comment='总价(万元)')   #总价
    UnitPrice = Column(Float,default=0,comment='单价(元/平米)')    #单价
    Apartment = Column(String(10),default='None',comment='户型')  #户型
    Area = Column(Float,default=0,comment='面积(平米)')
    Orientation = Column(String(10),default='None',comment='朝向')
    Renovation = Column(String(10),default='None',comment='装修')
    Floor = Column(String(15),default='None',comment='楼层')
    Construction_time = Column(String(15),default='None',comment='修建时间')
    Characteristics_apartment = Column(String(15),default='None',comment='户型特点')
    Follow = Column(Integer,default=0,comment='关注人数')
    Release_time = Column(Date,comment='发布时间')
    Modify_time = Column(DateTime,nullable=False, server_default=func.now(), onupdate=func.now())

class NewHouse(Base):
    __tablename__ = 'new_house'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    # Name,District,Probably_Location,Location,Price
    Title = Column(String(64), primary_key=True,comment='小区名字')  #帖子名字
    District = Column(String(10),nullable=False,comment='区')    #小区名字
    Probably_Location = Column(String(50), default='None', comment='大概位置')
    Location = Column(String(50),default='None',comment='具体位置')   #位置
    Price = Column(Float,default=0,comment='单价(元/平米)  均价')    #单价
    Modify_time = Column(DateTime,nullable=False, server_default=func.now(), onupdate=func.now())

class renthouse(Base):
    __tablename__ = 'rent_house'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    #Title,Rentway,District,Probably_Location,Location,Area,Orientation,Apartment,Floor,Price,Release_time,Modify_time
    Title = Column(String(64), primary_key=True, comment='小区名字')  # 帖子名字
    Rentway = Column(Integer,nullable=False,server_default='0',comment='出租方式 0：整租 1：合租 3：未知')
    District = Column(String(10), nullable=False, comment='区')
    Probably_Location = Column(String(50), server_default='None', comment='大概位置')
    Location = Column(String(50), server_default='None', comment='具体位置')  # 位置
    Area = Column(Float, server_default='0', comment='面积')
    Orientation = Column(String(10), server_default='None', comment='朝向')
    Apartment = Column(String(10), server_default='None', comment='户型')  # 户型
    Floor = Column(String(15), server_default='None', comment='楼层')
    Price = Column(Float, server_default='0', comment='单月价格')
    Release_time = Column(Date, comment='发布时间')
    Modify_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

















    # def save(self):
    #     Session = sessionmaker(bind=engine)
    #     session = Session()
    #     session.add(self)
    #     session.commit()

Base.metadata.create_all(engine)

# Session = sessionmaker(bind = engine)
# session = Session()
# fakers= [user(name= faker.name(),phone=faker.phone_number()) for i in range(20)]
# session.add_all(fakers)
# session.commit()
# session.close()

