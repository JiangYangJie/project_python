# -*-coding:utf8-*-
#     create by : JiangYangJie
#     email     : JiangYangJie@126.com
#     filename  : scipy
#     data      : 2019/11/18
import time, sys, os
from datetime import timedelta, datetime
import requests, random
from lxml import etree
import threading
from Mysql import mysql
from IPPool import IPPOOL
from get_headers import get_headers

# 给html文件添加目录
if not os.path.exists('./html'):
    os.makedirs('./html')
ips = IPPOOL().get_ips(numbers=40, flag=0)
headers = get_headers()


class Scipy():
    def __init__(self):
        pass

    def get_html(self, url, Page):
        head = {'User-Agent': random.choice(headers)}
        proxies = random.choice(ips)
        prox = {proxies.split(":", 1)[0]: proxies}
        try:
            response = requests.get(url, headers=head, proxies=prox)
            if response.status_code == 200:
                # print(url)
                with open('./html/house{}.html'.format(Page), 'wb') as f:
                    f.write(response.content)
                    # print(page)
        except Exception as e:
            print(e)

    def get_time(self, time_str):
        Time = ''.join(filter(str.isdigit, time_str))
        if Time == '':
            Day = 0
        else:
            if '月' in time_str:
                Day = int(Time) * 30
            elif '日' or '天' in time_str:
                Day = int(Time)
            elif '年' in time_str:
                Day = int(Time) * 365
            else:
                Day = 0
        return (datetime.now() - timedelta(days=Day)).strftime("%Y-%m-%d")


class Second_Hand_Scipy(Scipy):
    def __init__(self, url, page):
        Scipy.__init__(self)
        self.url = url
        self.page = page

    def deal_html(self):
        # print(self.url,page,self.page)
        # https: // cd.lianjia.com / ershoufang / pg50 / 50 50
        # https: // cd.lianjia.com / ershoufang / pg51 / 51 51
        # https: // cd.lianjia.com / ershoufang / pg52 / 52 52
        # https: // cd.lianjia.com / ershoufang / pg53 / 53 53
        # https: // cd.lianjia.com / ershoufang / pg54 / 54 54
        self.get_html(self.url, self.page)  # 此处self.url,self.page被暗改
        # 原因，只初始化了，一个对象，造成初始化后，self的值指向最后调用的方法
        # 造成程序有时，，传参成为一个问题
        # 为解决问题，因依次创建对象，不能只创建一个，每个对象应该调用自己的方法，这样才不会造成参数出现问题
        # print(self.page, page,self.url)
        # 54 51 https: // cd.lianjia.com / ershoufang / pg54 /
        # 54 50 https: // cd.lianjia.com / ershoufang / pg54 /
        # 54 52 https: // cd.lianjia.com / ershoufang / pg54 /
        # 54 54 https: // cd.lianjia.com / ershoufang / pg54 /
        # 54 53 https: // cd.lianjia.com / ershoufang / pg54 /
        try:
            with open('./html/house{}.html'.format(self.page), 'r', encoding='utf-8') as f:
                response = f.read()
            html = etree.HTML(response)
            title = html.xpath(r"//div[@class='info clear']/div[@class='title']/a//text()")
            # 2 的倍数
            positionInfo = html.xpath(r"//div[@class='positionInfo']/a//text()")
            # 3 的倍数
            priceInfo = html.xpath(r"//div[@class='info clear']/div[@class='priceInfo']//text()")
            houseInfo = html.xpath(r"//div[@class='houseInfo']//text()")
            followInfo = html.xpath(r"//div[@class='followInfo']//text()")
            return title, positionInfo, priceInfo, houseInfo, followInfo
        except Exception as e:
            print('deal_html', e)
            return [], [], [], [], []

    def deal_info(self):
        HouseInfo = []
        position = []
        price = []
        house = []
        follow = []
        title, positionInfo, priceInfo, houseInfo, followInfo = self.deal_html()
        info_lenth = len(title)
        if info_lenth < 5:
            return []
        for _ in range(info_lenth):  # 分割，提取，合并
            position.append([positionInfo[_ * 2], positionInfo[_ * 2 + 1]])
            price.append([priceInfo[_ * 3], priceInfo[_ * 3 + 2]])
            house.append(str(houseInfo[_]).split('|'))
            follow.append(str(followInfo[_]).split('/'))
            # number = filter(str.isdigit, my_str)
        for _ in range(info_lenth):  # str--》number
            price[_][1] = ''.join(filter(str.isdigit, price[_][1]))
            house[_][1] = house[_][1].split("平米")[0].split(' ')[
                1]  # ''.join(filter(str.isdigit or str=='.', house[_][1]))
            follow[_][0] = ''.join(filter(str.isdigit, follow[_][0]))
            follow[_][1] = self.get_time(follow[_][1])
            with mysql() as sql:
                readinfo = sql.read("select Title from second_hand where Title=%s", title[_])
            if len(readinfo) == 0:  # 没有相关内容，加到数据库里
                try:
                    HouseInfo.append([title[_], position[_][0], position[_][1], float(price[_][0]), float(price[_][1]),
                                      house[_][0], float(house[_][1]), house[_][2], house[_][3], house[_][4],
                                      house[_][5], house[_][6], int(follow[_][0]), follow[_][1]])
                except:
                    pass
                # print(len(position[_]),len(price[_]),len(house[_]),len(follow[_]))
        return HouseInfo

    def run(self):
        # sqlalchemy 对大数据量的插入没pymysql用起舒服
        # mutex.acquire()  # 取得锁
        data = self.deal_info()  # 不能方with里
        # print(data)
        # mutex.release()  # 释放锁
        with mysql() as sql:
            sql.write("insert ignore into second_hand("
                      "Title,Cellname,Location,Totalprice,UnitPrice,Apartment,Area,Orientation,Renovation,Floor,Construction_time,Characteristics_apartment,Follow,Release_time"
                      ") values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)


class NewHouse(Scipy):
    def __init__(self, url, page):
        Scipy.__init__(self)
        self.page = page
        self.url = url

    def deal_html(self):
        self.get_html(self.url, self.page)
        try:
            with open('./html/house{}.html'.format(self.page), 'r', encoding='utf-8') as f:
                response = f.read()
            html = etree.HTML(response)
            Name = html.xpath(r"//div[@class='resblock-name']/a//text()")
            District = html.xpath(r"//div[@class='resblock-location']//text()")
            Price = html.xpath(r"//div[@class='main-price']/span[@class='number']//text()")
            return Name, District, Price
        except Exception as e:
            print("deal_html:", e)
            return [], [], []

    def deal_info(self):
        info = []
        name, location, price = self.deal_html()
        try:
            lenth = int(len(location) / 11)
            Location = [[location[_ * 11 + 1], location[_ * 11 + 5], location[_ * 11 + 9]] for _ in range(lenth)]
            for _ in range(lenth):
                try:
                    price[_] = float(price[_])
                except:
                    price[_] = 0.0
                with mysql() as sql:
                    readinfo = sql.read("select Title from new_house where Title=%s", name[_])
                if len(readinfo) == 0:  # 没有相关内容，加到数据库里
                    info.append([name[_], Location[_][0], Location[_][1], Location[_][2], price[_]])
                # print(name[_], Location[_][0], Location[_][1], Location[_][2], price[_])
        except Exception as e:
            print(e)
        return info

    def run(self):
        data = self.deal_info()
        print(data)
        with mysql() as sql:
            sql.write("insert IGNORE into new_house("
                      "Title,District,Probably_Location,Location,Price"
                      ") values(%s,%s,%s,%s,%s)", data)


class RentHouse(Scipy):
    def __init__(self, url, page):
        Scipy.__init__(self)
        self.url = url
        self.page = page

    def deal_html(self):
        self.get_html(self.url, self.page)
        try:
            with open('./html/house{}.html'.format(self.page), 'r', encoding='utf-8') as f:
                response = f.read()
            html = etree.HTML(response)
            Name = html.xpath(r"//p[@class='content__list--item--title twoline']/a//text()")
            District = html.xpath(r"//p[@class='content__list--item--des']//text()")
            Price = html.xpath(r"//span[@class='content__list--item-price']/em//text()")
            Time = html.xpath(r"//p[@class='content__list--item--time oneline']//text()")
            return Name, District, Price, Time
        except Exception as e:
            print("deal_html:", e)
            return [], [], []

    def deal_info(self):
        # Title, Rentway, District, Probably_Location, Location, Area, Orientation, Apartment, Floor, Price, Release_time, Modify_time
        title, district, price, times = self.deal_html()
        lenght = int(len(district) / 17)
        renttype = [1 if '合' in _ else 0 for _ in title]
        timeS = [self.get_time(_) for _ in times]
        # print(len(title),len(price),lenght)        #filter(str.isdigit, price[_][1]))
        location = []
        try:
            for _ in range(lenght):
                location.append(
                    [title[_].strip(), renttype[_], district[_ * 17 + 1], district[_ * 17 + 3], district[_ * 17 + 5],
                     int(district[_ * 17 + 8].strip().split('㎡')[0]), district[_ * 17 + 10].strip(),
                     district[_ * 17 + 12].strip()
                        , district[_ * 17 + 15].strip().replace(' ', ''), int(price[_]), timeS[_]])
        except:
            pass
        return location

    def run(self):
        data = self.deal_info()
        # print(data)
        with mysql() as sql:
            sql.write("insert IGNORE into rent_house("
                      "Title, Rentway, District, Probably_Location, Location, Area, Orientation, Apartment, Floor, Price, Release_time"
                      ") values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)


class ScipyThread(threading.Thread):
    def __init__(self, name, objects):
        threading.Thread.__init__(self, name=name)
        self.name = name
        self.objects = objects

    def run(self):
        # print('start:',self.name)
        self.objects.run()
        # print('end:', self.name)
