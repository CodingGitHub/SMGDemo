'''
Created on 2017年4月1日

@author: lkl51
'''
import requests
import json


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
# list = ['http:///baike.baidu.com/view/824752.htm','http:///baike.baidu.com/view/824752.htm']
# postdata = {'task_id':'1491047322','task_period':'20180324_0046','apiinput':'1','urllist[]':list,'urluniq':'0'}
# data = requests.post('http://120.27.27.83:8081/api/task/taskstart?key=',data=postdata)
# print(data.json())


# peoplelistdata = requests.get('http://120.27.27.83:8081/api/data/getspiderconsolidateddata?key=&task_id=1491037886&task_period=20170324_0035&data_name=&pgfrom=&pgsize=').json()
# data = peoplelistdata['data']
# peoplelist = []
# for json_data in data:
# #     print(json_data['data_json'])
#     js_data = 'https://baike.baidu.com/' + eval(json_data['data_json'])['url']
#     peoplelist.append(js_data)
    

# print(peoplelist)
# print(data.json())
import time
print(int(time.time()))
time.sleep(30)
print(int(time.time()))



