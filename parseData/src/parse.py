'''
Created on 2017年3月30日

@author: lkl51
'''

import requests
# import json
import MySQLdb
from person import Person
import time
from taskOperate import Operator
from bokeh.util.logconfig import level
#数据解析类
class Parse:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.regionString = None
        self.organizeString = None
        self.PTag = None
        self.person = None
        self.operator = Operator()
        self.currentPersonId = None  #当前人物ID
        self.CurrentEntityId = None   #当前实体ID
    def createConnection(self,host='120.27.27.83',user='media_demo_user',passwd='6yhnMJU&',db='media_demo',port=20002):
        try:
            self.conn = MySQLdb.connect(host,user,passwd,db,port)
            self.conn.set_character_set('utf8')
            self.cur = self.conn.cursor()
            self.cur.execute("set names utf8")
            self.cur.execute('SET CHARACTER SET utf8;')
            self.cur.execute('SET character_set_connection=utf8;')
            print('数据库连接成功！')
        except Exception as e:
            print('数据库连接失败！')
            raise e
        
    def closeConnection(self):
        if self.conn:
            self.conn.close()
    
    
    def getDataFromCaiYunAPI(self,url):
        data = requests.get(url).json()
        if len(data['data']) <= 0:
            print('取出数据为空！！')
        return data
    
    
    #调用API得到的数据，并解析数据得到data的value下 的data_json的value    
    def parseTaskAData(self,key='',task_id='1491037886',task_period='20170324_0035',data_name='',pgfrom='',pgsize=''):
        url = "http://120.27.27.83:8081/api/data/getspiderconsolidateddata?key=%s&task_id=%s&task_period=%s&data_name=%s&pgfrom=%s&pgsize=%s"%(key,task_id,task_period,data_name,pgfrom,pgsize)
#         print(url)
        data = self.getDataFromCaiYunAPI(url)
#         print(jsn)
#         print(jsn.keys())
#         print(jsn['data'])
#         print(data)
        peopledict = {}
        for index,d in enumerate(data['data']):
            peopledict['title'] = eval(d['data_json'])['title']
            peopledict['url'] = 'https://baike.baidu.com' + eval(d['data_json'])['url']
            print(index,peopledict)
            urllist = []
            urllist.append(url)
#             print(self.execuTaskB(urllist))
            peopledata = self.execuTaskB(urllist = urllist)
            self.parseEntitydataFromTaskB(peopledata, level=1)

#             yield peopleInfoJson
    
    def execuTaskB(self, task_id = '1491047322', task_period = None, apiinput = '1', urllist = None, urluniq = '0'):
        data = {}
        data['task_id'] = task_id
        data['task_period'] = task_period
        data['apiinput'] = apiinput
        data['urllist[]'] = urllist
        data['urluniq'] = urluniq
        
        task_period = str(time.strftime('%y%m%d_%H%Mauto',time.localtime(time.time())))
        data['task_period'] = task_period
        
        return self.operator.getTaskResult(data)

    def parseEntitydataFromTaskB(self,entityData,level = 1):

        entityInfoDict = {}  
        entity_list = []

        
        for data in entityData:
            jsondata = eval(data['data_json'])
            print(type(jsondata))
    
    
            #目录
            if jsondata['data_name'] == 'catalog':
                seed_url = jsondata['_SEED_URL']
                if seed_url not in entityInfoDict:
                    entityInfoDict[seed_url] = {}
                entityInfoDict[seed_url]['catalog_name'] = jsondata['catalog_name']
                #url
                entityInfoDict[seed_url]['url'] = seed_url
            
            #名片
            if jsondata['data_name'] == 'entity_detail':
                basic_name = jsondata['basic_name']
                basic_value = jsondata['basic_value']
                nameList = basic_name.split('|')
                valueList = basic_value.split('|')
                str = ''
                for i in range(len(nameList)):
                    str += nameList[i].strip() + ':' + valueList[i].strip() + ';'            
                    print(basic_name,basic_value)
                    print(str)
                seed_url = jsondata['_SEED_URL']
                if seed_url not in entityInfoDict:
                    entityInfoDict[seed_url] = {}
                entityInfoDict[seed_url]['entity_detail'] = str
            
            #图片url
            if jsondata['data_name'] == 'entity_image':
                seed_url = jsondata['_SEED_URL']
                if seed_url not in entityInfoDict:
                    entityInfoDict[seed_url] = {}
                entityInfoDict[seed_url]['entity_image'] = jsondata['entity_image']
            
            #标签
            if jsondata['data_name'] == 'entity_tag':
                seed_url = jsondata['_SEED_URL']
                if seed_url not in entityInfoDict:
                    entityInfoDict[seed_url] = {}
                entityInfoDict[seed_url]['entity_tag'] = jsondata['entity_tag']
                #名字
                entityInfoDict[seed_url]['entity_name'] = jsondata['entity_name']
            
            #详细介绍
            if jsondata['data_name'] == 'introduction':
                seed_url = jsondata['_SEED_URL']
                if seed_url not in entityInfoDict:
                    entityInfoDict[seed_url] = {}
                entityInfoDict[seed_url]['introduction'] = jsondata['entity_intro']
            
            #全文
            if jsondata['data_name'] == 'text':
                seed_url = jsondata['_SEED_URL']
                if seed_url not in entityInfoDict:
                    entityInfoDict[seed_url] = {}
                entityInfoDict[seed_url]['text'] = jsondata['text_file']
            
            
            #子链接
            if jsondata['data_name'] == 'entity_list':
                seed_url = jsondata['_SEED_URL']
                if seed_url not in entityInfoDict:
                    entityInfoDict[seed_url] = {}
                    entityInfoDict[seed_url]['entitylist'] = []
        #         entiList = entityInfoDict[seed_url]['entity_list']
                for x in jsondata['url_list'].split('|'): 
                    if x != '':
                        entity_list.append('http:/baike.baidu.com' + x)
        entityInfoDict[seed_url]['entity_list'] = entity_list
        self.afterParseDataFromTaskB(entityInfoDict, level)
        
    def afterParseDataFromTaskB(self,entityInfoDict,level = 1):
        if level == 1:
            self.extractPerson(entityInfoDict, level = 1)
            urllist = entityInfoDict.items()[0]['entity_list']
            entitydata = self.execuTaskB(urllist = urllist)
            self.parseEntitydataFromTaskB(entitydata, level = 2)
        if level == 2:
            for key in entityInfoDict.keys():
                tag = entityInfoDict[key]['entity_tag']
                name = entityInfoDict[key]['entity_name']
                type = self.getEntityType(name, tag)
                if type == 1:
                    self.afterParseDataFromTaskB(entityInfoDict, level = 2)
            
        
    
    def extractPerson(self,entityInfo,level = 1):
        
        
        for key in entityInfo.keys():
            person = Person()
            person.setName(entityInfo[key]['entity_name'])
            person.setUrl(entityInfo[key]['url'])
            person.setImageUrl(entityInfo[key]['entity_image'])
            person.setCatalog(entityInfo[key]['catalog_name'])
            person.setIntroduction(entityInfo[key]['introduction'])
            person.setDetail(entityInfo[key]['entity_detail'])
            person.setReference(entityInfo[key]['text_file'])
            person.setTag(entityInfo[key]['entity_tag'])
            
            self.person = person
            
            dao = Dao()
            dao.insert('t_person', person, self.cur,self.conn)
            
            if not self.conn:
                self.createConnection()
                
            dao = Dao()
            if level == 1:
                self.currentPersonId = dao.insert('t_person', person, self.cur,self.conn)
            if level == 2:
                self.CurrentEntityId = dao.insert('t_person', person, self.cur,self.conn)
            
    #读地域字典
    def readRegiondict(self):       
        with open('region.txt','r',encoding = 'utf-8') as f:
            self.regionString = f.read()
        #print(self.regionString)
        
    #读组织机构字典
    def readOrganizedict(self):
        with open('organize.txt','r',encoding = 'utf-8') as e:
            self.organizeString = []
            str = e.readline()
            while str:
                self.organizeString.append(str)
                str = e.readline()
    
    #返回数据： 1:人物；2：地域；3：机构    None:其他
    def getEntityType(self,entityName,entityTag):
        if not self.regionString:
            self.readRegiondict()
        
        if not self.organizeString:
            self.readOrganizedict()
        
        entityNT = entityName + entityTag
        PTag = '人物'
        if entityName in self.regionString:
            return 2 
        for ora in self.organizeString:
            if (ora.strip() in entityNT):#strip()去除换行符
                return 3
        if PTag in entityTag:
            return 1
        else:
            return None

#数据库操作类
class Dao():
    #实现向数据库中people表中插入数据，并返回插入对象在数据库中的ID
    def insert(self,tableName,person,cur,conn):
        str = 'INSERT INTO %s(Name,URL,Introduction,BasicInfo,Catalog,Reference,Tag,ImageUrl,Detail) VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s")'%(tableName,person.getName(),person.getUrl(),person.getIntroduction(),person.getBasicInfo(),person.getCatalog(),person.getReference(),person.getTag(),person.getImageUrl(),person.getDetail())
        print(str)
        print(cur.execute(str))
        conn.commit()
        return cur.execute('select @@IDENTITY;')            
    
def main():
    p = Parse()
#     p.createConnection()
#     p.parseEntitydata()
    p.parseTaskAData()

if __name__ == '__main__':
    main()