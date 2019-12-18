# -*-coding:utf8-*- 
#     create by : JiangYangJie             
#     email     : JiangYangJie@126.com     
#     filename  : IPPool   
#     data      : 2019/11/11
# 使用前需创建表单 ip
# +-------------+-------------+------+-----+-------------------+-----------------------------------------------+
# | Field       | Type        | Null | Key | Default           | Extra                                         |
# +-------------+-------------+------+-----+-------------------+-----------------------------------------------+
# | proxies     | varchar(36) | NO   | PRI | NULL              |                                               |
# | create_time | timestamp   | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED                             |
# | update_time | timestamp   | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |
# +-------------+-------------+------+-----+-------------------+-----------------------------------------------+
#  自行修改数据库参数即可
import random
import re,sys
import requests
from lxml import etree
from Mysql import mysql
import get_headers as headers



class IPPOOL():
    def __init__(self):
        self.url='http://www.89ip.cn/index_{}.html'
        header =headers.get_headers()
        self.header = {'User-Agent':random.choice(header)}
        self.page=0

    def get_html(self):
        """
        :param page: 需要爬取的网页索引
        """
        response=requests.get(url=self.url.format(self.page), headers=self.header)
        if response.status_code==200:
            with open('./html/ip.html','wb') as f:
                f.write(response.content)
            return True
        else:
            return False

    def deal_html(self):
        ip_list = []
        if self.get_html():
            with open('./html/ip.html','r',encoding='utf-8') as f:
                response=f.read()
                html = etree.HTML(response)
            ip_info = ''.join(html.xpath(r'//table//tbody//tr//text()'))
            all_info = re.findall(r'\n\t\t\t(.*?)\t\t', ip_info)
            L = int(len(all_info) / 4)
            for i in range(L):
                Indexes = i * 4
                host = all_info[Indexes]
                port = all_info[Indexes + 1]
                location = all_info[Indexes + 2]
                update = all_info[Indexes + 3]
                ip_list.append([host, port, location, update])
            return ip_list
        else:
            return ip_list

    def testing_ip(self):
        url_list = ['https://www.sogou.com/','http://www.baidu.com','https://cn.bing.com/']
        ip_list=self.deal_html()
        ip = []
        for _ in range(len(ip_list)):
            IP=str(ip_list[_][0])+':'+str(ip_list[_][1])
            Url=random.choice(url_list)
            print('第{}页，第{}个ip开始校验'.format(self.page,_))
            try:
                proxies ={'http': 'http://'+IP}
                if requests.get(Url,self.header,proxies=proxies,timeout=2).status_code==200:
                    ip.append(['http://'+IP])
                    # print(proxies,'http 成功')
                else:
                    proxies = {'https': 'https://' + IP}
                    if requests.get(Url, self.header, proxies=proxies, timeout=2).status_code == 200:
                        ip.append(['https://'+IP])
                        # print(proxies, 'https 成功')
                print(proxies, '成功')
            except Exception as e:
                print(e)
                # print('第{}个失败'.format(_))
        return ip

    def ip_sql(self,number=30):
        with mysql(db='scipy') as sql:
            all_ip=sql.read("select proxies from ip")
            if len(all_ip)!=0:
                bad_ip = self.testing_sql_ip(all_ip)
                sql.write(" delete from ip where proxies=%s", bad_ip)
                print("当前数据库有{}有效代理，{}个无效代理".format(len(all_ip), len(bad_ip)))
            while(1):
                all_ip=sql.read("select proxies from ip")
                ip_lenth = len(all_ip)
                if ip_lenth <number:
                    self.page += 1
                    ip_list=self.testing_ip()
                    sql.write("insert into ip(proxies) values(%s)",ip_list)
                # else:
                    # bad_ip=self.testing_sql_ip(all_ip)
                    # sql.write(" delete from ip where proxies=%s",bad_ip)
                    # print("当前数据库有{}个有效代理.".format(len(all_ip)+ip_lenth))
                else:
                    print("IP池以装满，当前ip池代理数量",ip_lenth)
                    break


    def testing_sql_ip(self,proxies_list):
        url_list = ['https://www.sogou.com/', 'http://www.baidu.com', 'https://cn.bing.com/']
        bad_ip=[]
        for i in proxies_list:
            print("数据库：正在验证",i[0])
            Url = random.choice(url_list)
            proxies = {i[0].split(":",1)[0]: i[0]}
            try:
                if requests.get(Url, self.header, proxies=proxies, timeout=2).status_code == 200:
                    print(proxies,'成功')
            except Exception as e:
                bad_ip.append(i[0])
                print(e)
        return bad_ip

    def get_ips(self,numbers=5,flag=0): #flag:  1:校验  0：不校验
        ips=bad_ip=[]
        with mysql(db='scipy') as sql:
            all_ip=sql.read("select proxies from ip order by rand() limit %s",numbers)
            lenth=len(all_ip)
            if flag==1:
                print("正在校验代理........")
                while(1):
                    bad_ip = self.testing_sql_ip(all_ip)
                    sql.write(" delete from ip where proxies=%s", bad_ip)
                    bad = len(bad_ip)
                    if bad == 0:
                        break
                    else:
                        with mysql(db='scipy') as Sql:
                            all_ip = Sql.read("select proxies from ip order by rand() limit %s", bad)
                        lenth = len(all_ip)
                        if lenth<numbers:
                            self.ip_sql(numbers)
            if lenth==0 or lenth<numbers:
                self.ip_sql(numbers)
                with mysql(db='scipy') as Sql:
                    all_ip = Sql.read("select proxies from ip order by rand() limit %s", numbers)
        for _ in range(numbers):
            ips.append(all_ip[_][0])
        return ips
# pool=IPPOOL()
# # pool.get_ips()