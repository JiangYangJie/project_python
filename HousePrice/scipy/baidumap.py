# -*-coding:utf8-*- 
#     create by : JiangYangJie             
#     email     : JiangYangJie@126.com     
#     filename  : baidumap   
#     data      : 2019/11/21                      

import requests,json,socket,hashlib
from urllib import parse

def sn(queryStr):
    encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
    rawStr = encodedStr + 'szgM07mOxCFG5rDH7lgzciTGOWWDZ4Dl'
    Sn =  hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest()
    return Sn

def getAddres(name):
    ak = 'RpB8fNF8dPHFgXbAGazxyMcc5j4eQvj5'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
    url = "http://api.map.baidu.com/place/v2/search?query={}&tag=小区&region=成都&output=json&ak={}".format(name,str(ak))
    Sn = sn(url[24:])
    URL = url+'&sn='+str(Sn)
    response = requests.get(url=URL, headers=headers)
    print(response.json())
    try:
        lat = response.json()['results'][0]['location']['lat']
        lng = response.json()['results'][0]['location']['lng']
        address = response.json()['results'][0]['address']
        province=response.json()['results'][0]['province']
        city = response.json()['results'][0]['city']
        area = response.json()['results'][0]["area"]
        return [lat,lng,address,province,city,area]
    except:
        return []

print(getAddres('太阳公元大厦'))


