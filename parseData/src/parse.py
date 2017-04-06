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
from relation import Relation
from region import Region
from institution import Institution
#数据解析类
class Parse:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.regionString = None
        self.organizeString = None
        self.PTag = None
        self.person = None
        self.entity = None
        self.operator = Operator()
        self.currentPersonId = None  #当前人物ID
        self.CurrentEntityId = None   #当前实体ID
        self.dao = Dao()
        self.f = open('log.txt','a+',encoding = 'utf-8')
    
    def __del__(self):
        self.f.write('\n\n\n\n\n\n')
    def createConnection(self,host='120.27.27.83',user='media_demo_user',passwd='6yhnMJU&',db='media_demo',port=20002):
        try:
            self.conn = MySQLdb.connect(host,user,passwd,db,port)
            self.conn.set_character_set('utf8')
            self.cur = self.conn.cursor()
            self.cur.execute("set names utf8")
            self.cur.execute('SET CHARACTER SET utf8;')
            self.cur.execute('SET character_set_connection=utf8;')
            print('数据库连接成功！')
            self.f.write('数据库连接成功！')
        except Exception as e:
            print('数据库连接失败！')
            self.f.write('数据库连接失败！')
            raise e
        
    def closeConnection(self):
        if self.conn:
            self.conn.close()
    
    
    def getDataFromCaiYunAPI(self,url):
        data = requests.get(url).json()
        if len(data['data']) <= 0:
            print('取出数据为空！！')
            self.f.write('取出数据为空！！')
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
#             self.f.write(index+peopledict)
            urllist = []
            urllist.append(peopledict['url'])
#             print(self.execuTaskB(urllist))
            peopledata = self.execuTaskB(urllist = urllist)
#             print(peopledata)
            self.parseEntitydataFromTaskB(peopledata, level=1)

#             yield peopleInfoJson
    
    def execuTaskB(self, task_id = '1491047322', task_period = None, apiinput = '1', urllist = None, urluniq = '1'):
        data = {}
        data['task_id'] = task_id
        data['apiinput'] = apiinput
        data['urllist[]'] = urllist
        data['urluniq'] = urluniq
        
        task_period = str(time.strftime('%Y%m%d_%H%M%Sauto',time.localtime(time.time())))
        data['task_period'] = task_period
        
        return self.operator.getTaskResult(data)

    def parseEntitydataFromTaskB(self,entityData,level = 1):

        entityInfoDict = {}  
        entity_list = []

        if entityData:
            for data in entityData:
                jsondata = eval(data['data_json'])
    #             print(type(jsondata))
        
        
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
    #                     print(basic_name,basic_value)
    #                     print(str)
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
                if jsondata['data_name'] == 'entity_info':
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
                    entityInfoDict[seed_url]['text_file'] = jsondata['text_file']
                
                
                #子链接
                if jsondata['data_name'] == 'entity_list':
                    seed_url = jsondata['_SEED_URL']
                    if seed_url not in entityInfoDict:
                        entityInfoDict[seed_url] = {}
                        entityInfoDict[seed_url]['entitylist'] = []
            #         entiList = entityInfoDict[seed_url]['entity_list']
                    for x in jsondata['url_list'].strip().split('|'): 
                        if x != '':
                            entity_list.append('http://baike.baidu.com' + x.strip())
            entityInfoDict[seed_url]['entity_list'] = entity_list
            print(entityInfoDict)
            self.afterParseDataFromTaskB(entityInfoDict, level)
        
    def afterParseDataFromTaskB(self,entityInfoDict,level = 1):
        if level == 1:
            for key in entityInfoDict.keys():
#                 print(entityInfoDict[key])
                self.extractPerson(entityInfoDict[key], level = 1)
                if 'entity_list' in entityInfoDict[key]:
                    urllist = entityInfoDict[key]['entity_list']
                    print('urllist:' + str(urllist))
                    if len(urllist):
                        for url in urllist:
                            li = []
                            li.append(url)
                            print(li)
                            entitydata = self.execuTaskB(urllist = li)
                            self.parseEntitydataFromTaskB(entitydata, level = 2)
        if level == 2:
            for key in entityInfoDict.keys():
                if 'entity_tag' in entityInfoDict[key]:
                    tag = entityInfoDict[key]['entity_tag']
                else :
                    tag = ""
                    
                if 'entity_name' in entityInfoDict[key]:    
                    name = entityInfoDict[key]['entity_name']
                else :
                    name = ""
                type = self.getEntityType(name, tag)
                if type == 1:
#                     self.afterParseDataFromTaskB(entityInfoDict, level = 2)
                    self.extractPerson(entityInfoDict[key], level = 2)
                    self.relation(type)
                if type == 2:
                    self.extractRegion(entityInfoDict[key])
                    self.relation(type)
                if type == 3:
                    self.extractInstitution(entityInfoDict[key])
                    self.relation(type)
                    
                    
            
    
    #关系解析，entityInfo为第二层实体的信息，相当于entityInfoDict[key]
    def relation(self,type):
        if self.CurrentEntityId and self.currentPersonId:
            relation = Relation()
            relation.setId1(self.currentPersonId)
            relation.setId2(self.CurrentEntityId)
            relation.setType(type)
            relation.setStrength(self.getRelationStrength(self.person.getDetail()))
            self.dao.insertRelation('t_relation', relation, self.cur, self.conn)
            self.CurrentEntityId = None
#             self.currentPersonId = None
        
    def getRelationStrength(self,text_file):
        s = text_file
        count = s.count(self.entity.getName())
        return count
   
    
    
    
        
    
    def extractPerson(self,entityInfo,level = 1):
        
#         print(type(entityInfo))
#         print(entityInfo)
#         for key in entityInfo.keys():
        person = Person()
        if 'entity_name' in entityInfo:
            person.setName(entityInfo['entity_name'])
        if 'url' in entityInfo:
            person.setUrl(entityInfo['url'])
        if 'entity_image' in entityInfo:
            person.setImageUrl(entityInfo['entity_image'])
        if 'catalog_name' in entityInfo:
            person.setCatalog(entityInfo['catalog_name'])
        if 'introduction' in entityInfo:
            person.setIntroduction(entityInfo['introduction'])
        if 'entity_detail' in entityInfo:
            person.setBasicInfo(entityInfo['entity_detail'])
        if 'text_file' in entityInfo:    
            person.setDetail(entityInfo['text_file'])
        if 'entity_tag' in entityInfo:    
            person.setTag(entityInfo['entity_tag'])
            
            
        if not self.conn:
            self.createConnection()

        if level == 1:
            self.person = person
            self.currentPersonId = self.dao.insertPerson('t_person', person, self.cur,self.conn)
        if level == 2:
            self.entity = person
            self.CurrentEntityId = self.dao.insertPerson('t_person', person, self.cur,self.conn)
    
    def extractInstitution(self,entityInfo):
        institution = Institution()
        if 'entity_name' in entityInfo:
            institution.setName(entityInfo['entity_name'])
        if 'url' in entityInfo:
            institution.setUrl(entityInfo['url'])
        if 'entity_image' in entityInfo:
            institution.setImageUrl(entityInfo['entity_image'])
        if 'catalog_name' in entityInfo:
            institution.setCatalog(entityInfo['catalog_name'])
        if 'introduction' in entityInfo:
            institution.setIntroduction(entityInfo['introduction'])
        if 'entity_detail' in entityInfo:
            institution.setBasicInfo(entityInfo['entity_detail'])
        if 'text_file' in entityInfo:    
            institution.setDetail(entityInfo['text_file'])
        if 'entity_tag' in entityInfo:    
            institution.setTag(entityInfo['entity_tag'])
            
        if not self.conn:
            self.createConnection()
            
        self.entity = institution
        self.dao.insertInstitution('t_institution', institution, self.cur, self.conn)
        
    
    def extractRegion(self,entityInfo):
        region = Region()
        if 'entity_name' in entityInfo:
            region.setName(entityInfo['entity_name'])
        if 'url' in entityInfo:
            region.setUrl(entityInfo['url'])
        if 'entity_tag' in entityInfo:    
            region.setTag(entityInfo['entity_tag'])
            
        if not self.conn:
            self.createConnection()
        self.entity = region
        self.dao.insertRegion('t_region', region, self.cur, self.conn)
            
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
    def insertPerson(self,tableName,person,cur,conn):
        str = "INSERT INTO %s(Name,URL,Introduction,BasicInfo,Catalog,Tag,ImageUrl,Detail) VALUES('%s','%s','%s','%s','%s','%s','%s','%s')"%(tableName,person.getName(),person.getUrl(),person.getIntroduction(),person.getBasicInfo(),person.getCatalog(),person.getTag(),person.getImageUrl(),person.getDetail())
        print(str)
#         self.f.write(str)
        try:
            print(cur.execute(str))
            conn.commit()
            cur.execute('select @@IDENTITY;')
            last_id = cur.fetchone()[0]
            print(last_id)
            return last_id
        except:
            pass
    def insertRelation(self,tableName,relation,cur,conn):
        str = "INSERT INTO %s(ID1,ID2,Type,Name,Strength) VALUES('%s','%s','%s','%s','%s')"%(tableName,relation.getId1(),relation.getId2(),relation.getType(),relation.getName(),relation.getStrength()) 
        print(str)
#         self.f.write(str)
        try:
            print(cur.execute(str))
            conn.commit()
            cur.execute('select @@IDENTITY;')
            last_id = cur.fetchone()[0]
            print(last_id)
            return last_id
        except:
            pass
        
    #实现向数据库中表region中插入数据，并返回插入对象在数据库中的ID
    def insertRegion(self,tableName,region,cur,conn):
        str = "INSERT INTO %s(Name,URL,Type,Tag)VALUES('%s','%s','%s','%s')"%(tableName,region.getName(),region.getUrl(),region.getType(),region.getTag())
        print(str)
        print(cur.execute(str))
        conn.commit()
        cur.execute('select @@IDENTITY;')
        last_id = cur.fetchone()[0]
        print(last_id)
        return last_id
    def insertInstitution(self,tableName,institution,cur,conn):
        str = "INSERT INTO %s(Name,URL,Introduction,BasicInfo,detail,Tag,ImageUrl,Catalog)VALUES('%s','%s','%s','%s','%s','%s','%s','%s')"%(tableName,institution.getName(),institution.getUrl(),institution.getIntroduction(),institution.getBasicInfo(),institution.getDetail(),institution.getTag(),institution.getImageUrl(),institution.getCatalog())
        print(str)
        print(cur.execute(str))
        conn.commit()
        cur.execute('select @@IDENTITY;')
        last_id = cur.fetchone()[0]
        print(last_id)
        return last_id
    def insertPersonevent(self,tableName,personevent,cur,conn):
        str = "INSERT INTO %s(PID,Date,Detail)VALUES('%s','%s','%s')"%(tableName,personevent.getPid(),personevent.getDate(),personevent.getDetail())
        print(str)
        print(cur.execute(str))
        conn.commit()
        cur.execute('select @@IDENTITY;')
        last_id = cur.fetchone()[0]
        print(last_id)
        return last_id
                  
    
def main():
    p = Parse()
#     p.createConnection()
#     p.parseEntitydata()
    p.parseTaskAData()

if __name__ == '__main__':
    main()