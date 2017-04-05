'''
Created on 2017年4月2日

@author: lkl51
'''

import time
import requests

class Operator:
    
    #立即执行任务函数，返回0表示开始执行
    def startTaskImme(self,data,url='http://120.27.27.83:8081/api/task/taskstart?key='):
        js = requests.post(url, data).json()
#         print(js)
        if not eval(js['data'].strip())['status']:
            print('[' + data['task_id']+ ':' + data['task_period'] + ']' + '  ' + '抓取任务开始执行...')
            return True
        else :
            print('[' + data['task_id']+ ':' + data['task_period'] + ']' + '  ' + '抓取任务启动失败!!!')
            return False
    
    #查看任务某个周期的执行情况,抓取成功返回True，失败返回False
    def getTaskPeriodStatus(self,task_id,task_period,url='http://120.27.27.83:8081/api/task/getperiodstatus?key=&task_id=%s&task_period=%s'):
        url = url %(task_id,task_period)
        js = requests.get(url).json()
        period_status = js['data'][0]['period_status']
        if period_status:
            print('[' + task_id + ':' + task_period + ']' + '  ' + '抓取数据成功...' )
            return True
        else:
            print('[' + task_id + ':' + task_period + ']' + '  ' + '抓取数据失败...' )
            return False
        
    def getTaskResult(self,data):
        task_id = data['task_id']
        task_period = data['task_period']
        if self.startTaskImme(data):
            time.sleep(3)
            status = self.getTaskPeriodStatus(task_id, task_period)
            i = 0
            while (not status) and (i < 200):
                time.sleep(4)
                status = self.getTaskPeriodStatus(task_id, task_period)
                ++i
            if(i == 100):
                print('抓取数据失败!!!')
                return None
            else:
                return self.getTaskData(task_id = task_id, task_period = task_period)
        return None
    
    def getTaskData(self,key='',task_id='1491037886',task_period='20170324_0035',data_name='',pgfrom='',pgsize=''):
        url = "http://120.27.27.83:8081/api/data/getspiderconsolidateddata?key=%s&task_id=%s&task_period=%s&data_name=%s&pgfrom=%s&pgsize=%s"%(key,task_id,task_period,data_name,pgfrom,pgsize)
        print(url)
        data = requests.get(url).json()
        if len(data['data']):
            print('获取数据成功')
            return data['data']
        else:
            print('获取数据失败')
        return None
            
        
# def main():
#     operator = Operator()
#     list = ['http://baike.baidu.com/link?url=wmK0qP28-peYSEVxJQOYB9plGz4qJXdLyDOdkyAygvHVtCewQauZSYEiihXL7YK9pNGH0CrUlE4JasM2EIk0TLDX-EM3C0n0RyU47ubDPYz55wE_WOz1VyZgy3rRR0nJ&qq-pf-to=pcqq.c2c','http://baike.baidu.com/item/%E9%87%91%E6%BB%89%E6%A4%8D']
#     postdata = {'task_id':'1491141020','task_period':'20170324_0038','apiinput':'0','urllist[]':list,'urluniq':'1'}
#     operator.startTaskImme(data=postdata)
#     operator.getTaskPeriodStatus('1491141020', '20170324_0038')
#     
# if __name__ == '__main__':
#     main()