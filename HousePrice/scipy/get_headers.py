# -*-coding:utf8-*- 
#     create by : JiangYangJie             
#     email     : JiangYangJie@126.com     
#     filename  : get_headers   
#     data      : 2019/11/12
#    在使用本脚本前，需要创建headers数据表
# mysql> create table headers(
#     -> header varchar(300) not null,
#     -> create_time  timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#     -> Remarks varchar(100) )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='headers'
#     -> ;
# 自己将自己的数据库配置在每个函数内，即可

from Mysql import mysql

remakes=[['淘宝浏览器2.0 on Windows 7 x64'],['猎豹浏览器2.0.10.3198 急速模式on Windows 7 x64'],['猎豹浏览器2.0.10.3198 兼容模式on Windows 7 x64'],
        ['猎豹浏览器2.0.10.3198 兼容模式on Windows XP x86 IE6'],['猎豹浏览器1.5.9.2888 急速模式on Windows 7 x64'],
         ['QQ浏览器7.0 on Windows 7 x64 IE9'],
         ['360安全浏览器5.0自带IE8内核版 on Windows XP x86 IE6'],['360安全浏览器5.0 on Windows XP x86 IE6'],
         ['360安全浏览器5.0 on Windows 7 x64 IE9'],['360急速浏览器6.0 急速模式 on Windows XP x86'],
         ['360急速浏览器6.0 急速模式 on Windows 7 x64'],
         ['360急速浏览器6.0 兼容模式 on Windows 7 x64 IE9'],['360急速浏览器6.0 IE9/IE10模式 on Windows 7 x64 IE9'],
         ['搜狗浏览器4.0 高速模式 on Windows XP x86'],['搜狗浏览器4.0 兼容模式 on Windows XP x86 IE6'],
         ['Waterfox 16.0 on Windows 7 x64'],['Firefox x64 on Ubuntu 12.04.1 x64'],
         ['Chrome x64 on Ubuntu 12.04.1 x64'],['Chrome x86 23.0.1271.64 on Windows 7 x64'],
         ['Chrome x86 10.0.648.133 on Windows 7 x64'],['IE9 x64 9.0.8112.16421 on Windows 7 x64'],
         ['IE9 x86 9.0.8112.16421 on Windows 7 x64'],['Firefox x64 3.6.10 on ubuntu 10.10 x64'],
         ['Chrome x64']
         ]
headers = [['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11'],
           ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER'],
           ['Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)'],
           ['Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)'],
           ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER'],
           ['Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)'],
           ['Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)'],
           ['Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)'],
           ['Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)'],
           ['Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)'],
           ['Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'],
           ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'],
           ['Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)'],
           ['Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)'],
           ['Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0'],
           ['Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)'],
           ['Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0'],
           ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'],
           ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'],
           ['Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16'],
           ['Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)'],
           ['Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'],
           ['Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'],
           ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/69.0.3497.100 Safari/537.36"]
           ]
def into_sql(host='localhost', password='admin',db='scipy', port=3306,):
    L=[]
    for _ in range(len(headers)):
        L.append([headers[_][0],remakes[_][0]])
    with mysql(host='localhost', password='admin',db='scipy', port=3306,) as sql:
        sql.write("insert into headers(header,Remarks) values (%s,%s)",L)

def get_headers(number=5,host='localhost', password='admin',db='scipy', port=3306,):
    l=[]
    with mysql(host='localhost', password='admin', db='scipy', port=3306, ) as sql:
        L=sql.read("select * from headers order by rand() limit %s",number)
    for _ in range(number):
        l.append(L[_][0])
    return l

