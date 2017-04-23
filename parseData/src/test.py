# -*- coding=utf-8 -*- 

'''
Created on 2017年4月1日

@author: lkl51
'''
import requests
import json
import re
# from collections import Counter
# from _ast import Dict
# data = requests.get('http://120.27.27.83:8081/api/data/getspiderconsolidateddata?key=&task_id=1490604212&data_name=&pgfrom=2&pgsize=1')
# print(data.json())
# # print(js)
#  
# print(data.json()['data'][0]['data_json'])

#查看任务列表
# data = requests.get('http://120.27.27.83:8081/api/task/gettasklist')

#获得任务最近的周期列表及状态
# data = requests.get('http://120.27.27.83:8081/api/task/getperiodlist?key=&task_id=1491037886&task_period=20170402_1452')

#查看任务某个周期的执行情况
# data = requests.get('http://120.27.27.83:8081/api/task/getperiodstatus?key=&task_id=1491047322&task_period=20180324_0045')

#启动、停止抓取任务，task_status 可以为ON或者OFF
# data = requests.get('http://120.27.27.83:8081/api/task/settaskstatus?key=&task_id=1491037886&task_status=ON')

#立即停止任务
# data = requests.get('http://120.27.27.83:8081/api/task/taskstop?key=&task_id=1491037886&task_period=20170324_0035')

#post
# list = ['http://baike.baidu.com/item/%E4%B8%AD%E5%9B%BD%E5%85%B1%E4%BA%A7%E5%85%9A', 'http://baike.baidu.com/item/%E4%B8%AD%E5%9B%BD%E4%BA%BA%E6%B0%91%E8%A7%A3%E6%94%BE%E5%86%9B']
# postdata = {'task_id':'1491047322','task_period':'01190324_0056ab','apiinput':'1','urllist[]':list,'urluniq':'0'}
# data = requests.post('http://120.27.27.83:8081/api/task/taskstart?key=',data=postdata)
# print(data.json())


# peoplelistdata = requests.get('http://120.27.27.83:8081/api/data/getspiderconsolidateddata?key=&task_id=1491037886&task_period=20170324_0038&data_name=&pgfrom=&pgsize=').json()
# data = peoplelistdata['data']
# peoplelist = []
# for json_data in data:
#     print(json_data['data_json'])
#     js_data = 'https://baike.baidu.com/' + eval(json_data['data_json'])['url']
#     peoplelist.append(js_data)
#        

# print(peoplelist)
# # print(data.json())
# import time
# print(int(time.time()))
# time.sleep(30)
# print(int(time.time()))
# 
# dit1 = {'name':'lilei','years':'18'}
# dit2 = {'name':'li','years':'12'}
# print(Counter(dit1) + Counter(dit2))




# data_json1 = {"_SEED_URL":"http://baike.baidu.com/item/%E9%87%91%E6%BB%89%E6%A4%8D","cataId":"","catalog_name":"1|人物履历|2|人物事件|3|人物评价","data_name":"catalog","siteId":24,"task_id":"1491047322","task_period":"20170404_1726"}
# data_json2 = {"_SEED_URL":"http://baike.baidu.com/item/%E9%87%91%E6%BB%89%E6%A4%8D","basic_name":"中文名|外文名|国\xa0\xa0\xa0\xa0籍|出生地|出生日期|职\xa0\xa0\xa0\xa0业|毕业院校","basic_value":"金滉植|Kim Hwang-Sik|韩国|韩国全罗南道长城郡|1948年|韩国监查院院长，韩国总理|韩国首尔大学","cataId":"","data_name":"entity_detail","siteId":24,"task_id":"1491047322","task_period":"20170404_1726"}
# print(data_json1 + data_json2)
 
# peoplelistdata = requests.get('http://120.27.27.83:8081/api/data/getspiderconsolidateddata?key=&task_id=1491047322&task_period=20170404_1726&data_name=&pgfrom=&pgsize=').json()
# entitydata = peoplelistdata['data']
# print(entitydata)
# print(len(entitydata))
# 
# 
# 
# entityInfoDict = {}
# entity_list = []
# 
# for data in entitydata:
#     jsondata = eval(data['data_json'])
#     print(type(jsondata))
#     print(jsondata)
#     
#     
#     #目录
#     if jsondata['data_name'] == 'catalog':
#         seed_url = jsondata['_SEED_URL']
#         if seed_url not in entityInfoDict:
#             entityInfoDict[seed_url] = {}
#         entityInfoDict[seed_url]['catalog_name'] = jsondata['catalog_name']
#         #url
#         entityInfoDict[seed_url]['url'] = seed_url
#     
#     #名片
#     if jsondata['data_name'] == 'entity_detail':
#         basic_name = jsondata['basic_name']
#         basic_value = jsondata['basic_value']
#         nameList = basic_name.split('|')
#         valueList = basic_value.split('|')
#         str = ''
#         for i in range(len(nameList)):
#             str += nameList[i].strip() + ':' + valueList[i].strip() + ';'            
#             print(basic_name,basic_value)
#             print(str)
#         seed_url = jsondata['_SEED_URL']
#         if seed_url not in entityInfoDict:
#             entityInfoDict[seed_url] = {}
#         entityInfoDict[seed_url]['entity_detail'] = str
#     
#     #图片url
#     if jsondata['data_name'] == 'entity_image':
#         seed_url = jsondata['_SEED_URL']
#         if seed_url not in entityInfoDict:
#             entityInfoDict[seed_url] = {}
#         entityInfoDict[seed_url]['entity_image'] = jsondata['entity_image']
#     
#     #标签
#     if jsondata['data_name'] == 'entity_tag':
#         seed_url = jsondata['_SEED_URL']
#         if seed_url not in entityInfoDict:
#             entityInfoDict[seed_url] = {}
#         entityInfoDict[seed_url]['entity_tag'] = jsondata['entity_tag']
#         #名字
#         entityInfoDict[seed_url]['entity_name'] = jsondata['entity_name']
#     
#     #详细介绍
#     if jsondata['data_name'] == 'introduction':
#         seed_url = jsondata['_SEED_URL']
#         if seed_url not in entityInfoDict:
#             entityInfoDict[seed_url] = {}
#         entityInfoDict[seed_url]['introduction'] = jsondata['entity_intro']
#     
#     #全文
#     if jsondata['data_name'] == 'text':
#         seed_url = jsondata['_SEED_URL']
#         if seed_url not in entityInfoDict:
#             entityInfoDict[seed_url] = {}
#         entityInfoDict[seed_url]['text'] = jsondata['text_file']
#     
#     
#     #子链接
#     if jsondata['data_name'] == 'entity_list':
#         seed_url = jsondata['_SEED_URL']
#         if seed_url not in entityInfoDict:
#             entityInfoDict[seed_url] = {}
#             entityInfoDict[seed_url]['entitylist'] = []
# #         entiList = entityInfoDict[seed_url]['entity_list']
#         for x in jsondata['url_list'].split('|'): 
#             if x != '':
#                 entity_list.append('http:/baike.baidu.com' + x)
# entityInfoDict[seed_url]['entity_list'] = entity_list
#     
#     
# print(entityInfoDict)

# url = 'dsada'
# print(list(url))     

# print("zhang'hao".replace("'", "''"))
# str  = '2011年1月14日6时，刘华清\在北京逝世，享年\\95岁。'
# pa1 = re.compile(r'^\d{4}年\d{0,2}月*\d{0,2}日*\d{0,2}时*')
# print( re.findall(pa1, str))
# print(sorted(['2011年1月14日6时','2011年','2011年1月']))
# str = str.replace('\\','').replace(',', '')
# print(str)
# import MySQLdb
# conn = MySQLdb.connect('120.27.27.83','media_demo_user','6yhnMJU&','media_demo',20002)
# cur = conn.cursor()
# conn.set_character_set('utf8')
# cur.execute("set names utf8")
# cur.execute('SET CHARACTER SET utf8;')
# cur.execute('SET character_set_connection=utf8;')
# print(cur.execute("select *from t_person t where t.URL = 'https://baike.baidu.com/view/1069807.htm'"))
# print(cur.fetchone())
#
# def qq():
#     return 1,2
# 
# print(qq())
# 
# 
# aa = list()
# aa.append(1)
# print(aa)
# 
# 
# bb = dict()
# bb['a'] = {}
# bb['a']['b'] = aa
# print(bb['a']['b'])


# import sys
# import os
# print(sys.path[0])
# print(os.getcwd())
# print(os.path.split(os.path.realpath(__file__))[0] )

# from bs4 import BeautifulSoup
# str = '<div class="para" label-module="para">《开国元勋画传》是2001年6月1日中央文献出版社出版的图书，作者吴殿尧。全书共四卷，200余万字，3800多幅图片，图文并茂，体例新颖、内容翔实。本画传介绍了<a target=_blank href="/item/%E6%AF%9B%E6%B3%BD%E4%B8%9C/113835" data-lemmaid="113835">毛泽东</a>、<a target=_blank href="/item/%E5%91%A8%E6%81%A9%E6%9D%A5">周恩来</a>、<a target=_blank href="/item/%E5%88%98%E5%B0%91%E5%A5%87">刘少奇</a>、<a target=_blank href="/item/%E6%9C%B1%E5%BE%B7">朱德</a>、<a target=_blank href="/item/%E6%9E%97%E5%BD%AA">林彪</a>、<a target=_blank href="/item/%E4%BB%BB%E5%BC%BC%E6%97%B6/34637" data-lemmaid="34637">任弼时</a>、<a target=_blank href="/item/%E9%82%93%E5%B0%8F%E5%B9%B3/116181" data-lemmaid="116181">邓小平</a>、<a target=_blank href="/item/%E9%99%88%E4%BA%91/26156" data-lemmaid="26156">陈云</a>、<a target=_blank href="/item/%E8%91%A3%E5%BF%85%E6%AD%A6">董必武</a>、<a target=_blank href="/item/%E5%AE%8B%E5%BA%86%E9%BE%84">宋庆龄</a>、<a target=_blank href="/item/%E5%BD%AD%E5%BE%B7%E6%80%80">彭德怀</a>、<a target=_blank href="/item/%E5%88%98%E4%BC%AF%E6%89%BF">刘伯承</a>、<a target=_blank href="/item/%E8%B4%BA%E9%BE%99">贺龙</a>、<a target=_blank href="/item/%E9%99%88%E6%AF%85/22586" data-lemmaid="22586">陈毅</a>、<a target=_blank href="/item/%E7%BD%97%E8%8D%A3%E6%A1%93">罗荣桓</a>、<a target=_blank href="/item/%E5%BE%90%E5%90%91%E5%89%8D">徐向前</a>、<a target=_blank href="/item/%E8%81%82%E8%8D%A3%E8%87%BB/116123" data-lemmaid="116123">聂荣臻</a>、<a target=_blank href="/item/%E5%8F%B6%E5%89%91%E8%8B%B1">叶剑英</a>等开国元勋伟大光辉的一生。</div>'
# page = BeautifulSoup(str,'lxml')
# hrefs = page.find_all('a')
# ss = []
# for item in hrefs:
#     ss.append('baike.baidu.com' + item['href'])
# print((ss))

import time
print(time.strftime('%H-%M-%S',time.localtime(time.time())))

