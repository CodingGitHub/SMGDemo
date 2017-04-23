# -*- coding=utf-8 -*-  
'''
Created on 2017年3月30日

@author: lkl51
'''

import requests
# import json
import re
# try:
#     import MySQLdb
# except:
import pymysql
#     pymysql.install_as_MySQLdb()
#     import MySQLdb

import sys
import os
sys.path.insert(0, os.path.split(os.path.realpath(__file__))[0])
from person import Person
import time
from taskOperate import Operator
from relation import Relation
from region import Region
from institution import Institution
from personevent import PersonEvent
import institution

#数据解析类
class Parse:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.regionString = None
        self.organizeString = None
        self.relationtypedict = dict()  #初始化定义一个关系类型字典
        self.relationdict = dict()   #初始化定义一个关系字典
        self.PTag = None
        self.person = None   #第一层人物
        self.entity = None  #第二层实体
        self.operator = Operator()  #执行采云任务类
        self.currentPersonId = None  #当前人物ID
        self.entityType = -1  #当前实体类型
        self.CurrentEntityId = None   #当前实体ID
        self.dao = Dao()
#         self.f = open('log.txt','a+',encoding = 'utf-8')
        self.unUsedUrlSet = set()  #存储已经抓取并且没有用到的实体（既不是人物，又不是地域和机构）
#         self.savedUrlSet = set()  #存储已经保存到数据库中的实体url
    
    def __del__(self):
#         self.f.write('\n\n\n\n\n\n')
        self.closeConnection()
#     def createConnection(self,host='localhost',user='root',passwd='',db='media_demo',port=3306):
    def createConnection(self,host='120.27.27.83',user='media_demo_user',passwd='6yhnMJU&',db='media_demo_test',port=20002):
        try:
            self.conn = pymysql.connect(host,user,passwd,db,port,use_unicode=True, charset="utf8")
#             self.conn.set_character_set('utf8')
            self.cur = self.conn.cursor()
            self.cur.execute("set names utf8")
            self.cur.execute('SET CHARACTER SET utf8;')
            self.cur.execute('SET character_set_connection=utf8;')
            print('数据库连接成功！')
#             self.f.write('数据库连接成功！')
        except Exception as e:
            print('数据库连接失败！')
#             self.f.write('数据库连接失败！')
            raise e
        
    def closeConnection(self):
        if self.conn:
            self.conn.close()
    
    
    def getDataFromCaiYunAPI(self,url):
        data = requests.get(url).json()
        if len(data['data']) <= 0:
            print('取出数据为空！！')
#             self.f.write('取出数据为空！！')
        return data
    
    
    #调用采云API得到的数据，并解析数据得到字典data的value下 的data_json的value    
    def parseTaskAData(self,key='',task_id='1491037886',task_period='20170413_1447',data_name='',pgfrom='',pgsize=''):
        url = "http://120.27.27.83:8081/api/data/getspiderconsolidateddata?key=%s&task_id=%s&task_period=%s&data_name=%s&pgfrom=%s&pgsize=%s"%(key,task_id,task_period,data_name,pgfrom,pgsize)
#         print(url)
        data = []
        with open('urllist.txt','r',encoding = 'utf-8') as f:
            listurl = f.readlines()
            for line in listurl:
                line=line.strip('\n')
                data.append(line)
            print(data)
        #data = ['baike.baidu.com/item/%E6%AF%9B%E6%B3%BD%E4%B8%9C/113835', 'baike.baidu.com/item/%E5%91%A8%E6%81%A9%E6%9D%A5', 'baike.baidu.com/item/%E5%88%98%E5%B0%91%E5%A5%87', 'baike.baidu.com/item/%E6%9C%B1%E5%BE%B7', 'baike.baidu.com/item/%E6%9E%97%E5%BD%AA', 'baike.baidu.com/item/%E4%BB%BB%E5%BC%BC%E6%97%B6/34637', 'baike.baidu.com/item/%E9%82%93%E5%B0%8F%E5%B9%B3/116181', 'baike.baidu.com/item/%E9%99%88%E4%BA%91/26156', 'baike.baidu.com/item/%E8%91%A3%E5%BF%85%E6%AD%A6', 'baike.baidu.com/item/%E5%AE%8B%E5%BA%86%E9%BE%84', 'baike.baidu.com/item/%E5%BD%AD%E5%BE%B7%E6%80%80', 'baike.baidu.com/item/%E5%88%98%E4%BC%AF%E6%89%BF', 'baike.baidu.com/item/%E8%B4%BA%E9%BE%99', 'baike.baidu.com/item/%E9%99%88%E6%AF%85/22586', 'baike.baidu.com/item/%E7%BD%97%E8%8D%A3%E6%A1%93', 'baike.baidu.com/item/%E5%BE%90%E5%90%91%E5%89%8D', 'baike.baidu.com/item/%E8%81%82%E8%8D%A3%E8%87%BB/116123', 'baike.baidu.com/item/%E5%8F%B6%E5%89%91%E8%8B%B1']
        peopledict = {}
        for index,d in enumerate(data):
#             peopledict['title'] = eval(d['data_json'])['title']
#             peopledict['url'] = 'https://baike.baidu.com' + eval(d['data_json'])['url']
            print(index,d)
            urllist = []
            urllist.append(d)
            peopledata = self.execuTaskB(urllist = urllist)
            self.parseEntitydataFromTaskB(peopledata, level=1)

    
    def execuTaskB(self, task_id = '1492499609', task_period = None, apiinput = '1', urllist = None, urluniq = '1'):
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
#                         entityInfoDict[seed_url]['entity_list'] = list()
#                     print(entityInfoDict[seed_url])
                    entiList = entityInfoDict[seed_url].setdefault('entity_list',[])
                    for x in jsondata['url_list'].strip().split('|'): 
                        if x != '':
                            entiList.append('http://baike.baidu.com' + x.strip())
                    entityInfoDict[seed_url]['entity_list'] = entiList
#             print(entityInfoDict)

                
                #家谱
                if jsondata['data_name'] == 'people_relation':
                    seed_url = jsondata['_SEED_URL']
                    if seed_url not in entityInfoDict:
                        entityInfoDict[seed_url] = {}
#                         entityInfoDict[seed_url]['entity_list'] = list()
#                     print(entityInfoDict[seed_url])
                    entiList = entityInfoDict[seed_url].setdefault('people_relation',[])
                    for x in jsondata['entity_url'].strip().split('|'): 
                        if x != '':
                            entiList.append(x.strip())
                    entityInfoDict[seed_url]['people_relation'] = entiList
            self.afterParseDataFromTaskB(entityInfoDict, level)
        
    def afterParseDataFromTaskB(self,entityInfoDict,level = 1):
        if level == 1:
            for key in entityInfoDict.keys():
#                 print(entityInfoDict[key])
                self.extractPerson(entityInfoDict[key], level = 1)
                
                urllist = []
                if 'entity_list' in entityInfoDict[key] :
                    urllist += entityInfoDict[key]['entity_list']
                if 'people_relation' in entityInfoDict[key]:
                    urllist += entityInfoDict[key]['people_relation']
#                     print('urllist:' + str(urllist))
                if len(urllist):
                    for url in urllist:
                        #过滤掉图片实体
                        if 'fr=lemma&ct=single' in url:
                            continue
                        
                        #判断之前是否已经抓取过，并且为没用的实体,如果抓取过，就跳过当前，进行下一个
                        if self.isSpiderUnused(url):
                            continue
                        
#                         判断是否已入库
                        m_type,m_entity = self.isInDatabase(url, ImageUrl = None, type = -1)
                        if m_type != -1: #已入库，则从库中得到实体信息
                            self.entity = m_entity
                            self.entityType = m_type
                            self.CurrentEntityId = m_entity.getId()
                            self.relationParse(self.entityType)
                        else:  #未入库，进行抓取
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
                if type == 1:#人物
                    self.extractPerson(entityInfoDict[key], level = 2)                    
                    self.relationParse(type)
                elif type == 2:#地域
                    self.extractRegion(entityInfoDict[key])
                    self.relationParse(type)
                elif type == 3:#机构
                    self.extractInstitution(entityInfoDict[key])
                    self.relationParse(type)
                else: #没用的实体
                    self.unUsedUrlSet.add(entityInfoDict[key]['url'])
    
    #判断是否之前已经抓取过，并且该url的实体没用到
    def isSpiderUnused(self,url):
        if len(self.unUsedUrlSet) > 100000:
            self.unUsedUrlSet.clear()
        return url in self.unUsedUrlSet
    
    #判断是否是已经保存到数据库中的url
#     def isSavedUrl(self,url):
#         if len(self.savedUrlSet) > 100000:
#             self.savedUrlSet.clear()
#         return url in self.savedUrlSet
        
    
    #分割全文（By句）
    def cutText(self,text_file):
        if  not isinstance(text_file,str): #判断是否为str类型
            text_file = str(text_file).strip()
        puzs = frozenset('。！？.!?;；') #划分标志结合
        tmp = []
        for ch in text_file: #遍历全文
            tmp.append(ch)
            if puzs.__contains__(ch):#判断是否为断句标志
                yield ''.join(tmp)
                tmp = []
        yield ''.join(tmp) 
    
    #提取事件和时间   
    def extractEvent(self,id,cutText):
#         print(list(cutText))
        regex1 = re.compile(r'\w*\d{2,4}年\d{0,2}月*\d{0,2}日*\d{0,2}时*')
        regex2 = re.compile(r'\d{2,4}年\d{0,2}月*\d{0,2}日*\d{0,2}时*')
        #判断是否正则表达式和句子匹配
        for subject in cutText:  #遍历文章中的每一句话
            if re.match(regex1,subject.strip()): #年
                #re.findall(regex,subject)
                #event = subject
                date = re.findall(regex2,subject.strip())[0]
                
                personevent = PersonEvent()
                personevent.setPid(id)
                personevent.setDate(date)
                personevent.setDetail(subject)#提取事件内容
                self.dao.insertPersonevent('t_personevent',personevent,self.cur,self.conn)
                
                            
    #关系解析，entityInfo为第二层实体的信息，相当于entityInfoDict[key]
    def relationParse(self,type):
        if self.CurrentEntityId and self.currentPersonId:
            relation = Relation()
            
            relation.setId1(self.currentPersonId)
            relation.setId2(self.CurrentEntityId)
            
            relation.setType(type)
#             if type == 1:
            name,des = self.judgeRelation(self.entity.getName(),self.cutText(self.person.getDetail()))
            relation.setName(name) #得到关系名称
            relation.setDescribe(des) #得到关系描述
            
            prtype = self.judgeRelationType(name)
            relation.setPrtype(prtype) #得到关系类别
            
            strength = self.getRelationStrength(self.person.getDetail())
            relation.setStrength(strength)
            self.dao.insertRelation('t_relation', relation, self.cur, self.conn)
            
            if type == 1:
                reverseRelation = Relation()
                reverseRelation.setId1(self.CurrentEntityId)
                reverseRelation.setId2(self.currentPersonId) 
                reverseRelation.setType(type)
    #             
                reverseRelation.setName(name) #得到关系名称
                reverseRelation.setDescribe(des) #得到关系描述
                
                reverseRelation.setPrtype(prtype) #得到关系类别
                reverseRelation.setStrength(strength)
                self.dao.insertRelation('t_relation', reverseRelation, self.cur, self.conn)
            
            
            self.CurrentEntityId = None
#             self.currentPersonId = None
    
    #读关系字典
    def readRelationdict(self):    
        with open('relation.txt','r',encoding = 'utf-8') as df:
            line = df.readline().strip()
            while(line):
                self.relationdict[line.split(' ')[0]] = line.split(' ')[1]
                line =df.readline().strip()
    
    #读关系类型字典
    def readRelationTypedict(self):
        with open('relationtype.txt','r',encoding = 'utf-8') as ef:
            line = ef.readline().strip()
            while(line):
                self.relationtypedict[line.split(' ')[0]] = line.split(' ')[1]
                line =ef.readline().strip()
                
    '''#提取实体的name
    def getNameByID(self,CurrentEntityId,cur,conn):
            CurrentEntityId = self.CurrentEntityId
            str = "SELECT Name FROM t_person where ID= %s"%(CurrentEntityId)
            print(str)
            try:
                print(cur.execute(str))
                conn.commit()
                secondName = cur.fetchone()[0]
                return secondName
            except:
                raise
    '''
    #判断关系名称，返回关系名称和关系描述                 
    def judgeRelation(self,secondName,cutText):
        if not self.relationdict:
            self.readRelationdict()
        if cutText:
            for subject in cutText:   #遍历文章中的每个句子
                if re.search(secondName,subject): #判断实体名字是否在句子中
                    for key in self.relationdict.keys(): #遍历关系字典
                        if key in subject: #判断称呼是否在句子中
                            return self.relationdict[key],subject #返回关系名称、关系描述
                    return None,subject
        return None,None
            
    '''#关系描述       
    def getRelationDescribe(self,secondName,cutText):
        for subject in cutText:   #遍历文章中的每个句子
            if re.search(secondName,subject): #判断实体名字是否在句子中
                return subject
    '''
            
    #判断关系类型-1.亲情 2.友情 3.爱情 4.工作 5.其他             
    def judgeRelationType(self,relationName):
        if not self.relationtypedict:
            self.readRelationTypedict()
        if relationName:
            if relationName in self.relationtypedict:
                rtype = self.relationtypedict[relationName]
                if rtype == '亲情':
                    return 1
                if rtype == '友情':
                    return 2
                if rtype == '爱情':
                    return 3
                if rtype == '工作':
                    return 4
        return 5
    
    #计算关系强度   
    def getRelationStrength(self,text_file):
        s = text_file
        count = s.count(self.entity.getName())
        return count        
    
    def extractPerson(self,entityInfo,level = 1):
        
#         print(type(entityInfo))
#         print(entityInfo)
#         for key in entityInfo.keys():
        person = Person()
        if 'entity_image' in entityInfo:
            imageUrl = entityInfo['entity_image']
            
            #根据ImageUrl判断是否数据库中已经存在该实体
            if imageUrl:
                m_entity = self.isInDatabase(url = None, ImageUrl = imageUrl, type = 1)[1]
                if m_entity:
                    if level == 1:
                        self.person = m_entity;
                        self.currentPersonId = m_entity.getId()
                    else:
                        self.entity = m_entity;
                        self.CurrentEntityId = m_entity.getId()
                    return
                        
            person.setImageUrl(imageUrl)
        if 'entity_name' in entityInfo:
            person.setName(entityInfo['entity_name'].replace("'","''").replace('\\',''))
        if 'url' in entityInfo:
            person.setUrl(entityInfo['url'])
        if 'catalog_name' in entityInfo:
            person.setCatalog(entityInfo['catalog_name'])
        if 'introduction' in entityInfo:
            person.setIntroduction(entityInfo['introduction'].replace("'","''").replace('\\',''))
        if 'entity_detail' in entityInfo:
            person.setBasicInfo(entityInfo['entity_detail'].replace("'","''").replace('\\',''))
        if 'text_file' in entityInfo:    
            person.setDetail(entityInfo['text_file'].replace("'","''").replace('\\',''))
        if 'entity_tag' in entityInfo:    
            person.setTag(entityInfo['entity_tag'])
            
            
        if not self.conn:
            self.createConnection()

        if level == 1:
            self.person = person
            self.currentPersonId = self.dao.insertPerson('t_person', person, self.cur,self.conn)
            self.extractEvent(self.currentPersonId, self.cutText(self.person.getDetail()))
        if level == 2:
            self.entity = person
            self.CurrentEntityId = self.dao.insertPerson('t_person', person, self.cur,self.conn)
            self.extractEvent(self.CurrentEntityId, self.cutText(self.entity.getDetail()))
            
        
#         self.savedUrlSet.add(person.getUrl())
        
    
    def extractInstitution(self,entityInfo):
        institution = Institution()
        if 'entity_image' in entityInfo:
            imageUrl = entityInfo['entity_image']
            
            if imageUrl:
                #根据ImageUrl判断是否数据库中已经存在该实体
                m_entity = self.isInDatabase(url = None, ImageUrl = imageUrl, type = 3)[1]
                if m_entity:
                    self.entity = m_entity;
                    self.CurrentEntityId = m_entity.getId()
                    return
            
            institution.setImageUrl(entityInfo['entity_image'])
        if 'entity_name' in entityInfo:
            institution.setName(entityInfo['entity_name'])
        if 'url' in entityInfo:
            institution.setUrl(entityInfo['url'])
        if 'catalog_name' in entityInfo:
            institution.setCatalog(entityInfo['catalog_name'])
        if 'introduction' in entityInfo:
            institution.setIntroduction(entityInfo['introduction'].replace("'","''").replace('\\',''))
        if 'entity_detail' in entityInfo:
            institution.setBasicInfo(entityInfo['entity_detail'].replace("'","''").replace('\\',''))
        if 'text_file' in entityInfo:    
            institution.setDetail(entityInfo['text_file'].replace("'","''").replace('\\',''))
        if 'entity_tag' in entityInfo:    
            institution.setTag(entityInfo['entity_tag'])
            
        if not self.conn:
            self.createConnection()
            
        self.entity = institution
        self.CurrentEntityId = self.dao.insertInstitution('t_institution', institution, self.cur, self.conn)
#         self.savedUrlSet.add(institution.getUrl())
    
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
        self.CurrentEntityId = self.dao.insertRegion('t_region', region, self.cur, self.conn)
#         self.savedUrlSet.add(region.getUrl())
            
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
        if entityName == "":
            return None
        
        
        entityNT = entityName + entityTag
        PTag = '人物'
        if entityName in self.regionString:
            return 2    #地域
        for ora in self.organizeString:
            if (ora.strip() in entityNT):#strip()去除换行符
                return 3  #组织机构
        if PTag in entityTag:
            return 1   #人物
        else:
            return None
        
    #判断实体是否存在数据库中，如果存在，返回实体信息，否则返回None，url为实体url，ImageUrl为图片url，type为实体类别    
    def isInDatabase(self,url = None, ImageUrl = None,type = -1):
        if not self.conn:
            self.createConnection()
        
        
        #根据url判别是否存在数据库中，由于此时不知道type，所以需要三个表逐次判别
        if url:
            res = self.dao.selectbyUrl('t_person', url, 'url', self.conn, self.cur)
            if res:
                return 1,res
            res = self.dao.selectbyUrl('t_region', url, 'url', self.conn, self.cur)
            if res:
                return 2,res
            res = self.dao.selectbyUrl('t_institution', url, 'url', self.conn, self.cur)
            if res:
                return 3,res
            
        #根据图片url和type判别是否存在数据库中
        elif ImageUrl:
            if type == 1:
                res = self.dao.selectbyUrl('t_person', ImageUrl, 'ImageUrl', self.conn, self.cur)
                if res:
                    return 1,res
            elif type == 2:
                res = self.dao.selectbyUrl('t_region', ImageUrl, 'ImageUrl', self.conn, self.cur)
                if res:
                    return 2,res
            elif type == 3:
                res = self.dao.selectbyUrl('t_institution', ImageUrl, 'ImageUrl', self.conn, self.cur)
                if res:
                    return 3,res
        return -1, None            

#数据库操作类
class Dao():
    #实现向数据库中people表中插入数据，并返回插入对象在数据库中的ID
    def insertPerson(self,tableName,person,cur,conn):
        str = "INSERT INTO %s(Name,URL,Introduction,BasicInfo,Catalog,Tag,ImageUrl,Detail) VALUES('%s','%s','%s','%s','%s','%s','%s','%s')"%(tableName,person.getName(),person.getUrl(),person.getIntroduction(),person.getBasicInfo(),person.getCatalog(),person.getTag(),person.getImageUrl(),person.getDetail())
        print('insert t_person:[name:%s]'%(person.getName()))
#         self.f.write(str)
        try:
            cur.execute(str)
            conn.commit()
            cur.execute('select @@IDENTITY;')
            last_id = cur.fetchone()[0]
            print(last_id)
            return last_id
        except:
            pass
        
    def insertRelation(self,tableName,relation,cur,conn):
        str = "INSERT INTO %s(ID1,ID2,Type,Name,RelationDescribe,Prtype,Strength) VALUES('%s','%s','%s','%s','%s','%s','%s')"%(tableName,relation.getId1(),relation.getId2(),relation.getType(),relation.getName(),relation.getDescribe(),relation.getPrtype() ,relation.getStrength()) 
        print('insert t_relation:[ID1:%s, ID2:%s, Type:%s]'%(relation.getId1(),relation.getId2(),relation.getType()))
#         self.f.write(str)
        
        try:
            cur.execute(str)
            conn.commit()
#             cur.execute('select @@IDENTITY;')
#             last_id = cur.fetchone()[0]
#             print(last_id)
#             return last_id
        except:
            pass
        
        
    #实现向数据库中表region中插入数据，并返回插入对象在数据库中的ID
    def insertRegion(self,tableName,region,cur,conn):
        str = "INSERT INTO %s(Name,URL,Type,Tag)VALUES('%s','%s','%s','%s')"%(tableName,region.getName(),region.getUrl(),region.getType(),region.getTag())
        print('insert t_region:[name:%s]'%(region.getName()) )
        try:
            cur.execute(str)
            conn.commit()
            cur.execute('select @@IDENTITY;')
            last_id = cur.fetchone()[0]
            print(last_id)
            return last_id
        except:
            pass
    def insertInstitution(self,tableName,institution,cur,conn):
        str = "INSERT INTO %s(Name,URL,Introduction,BasicInfo,detail,Tag,ImageUrl,Catalog)VALUES('%s','%s','%s','%s','%s','%s','%s','%s')"%(tableName,institution.getName(),institution.getUrl(),institution.getIntroduction(),institution.getBasicInfo(),institution.getDetail(),institution.getTag(),institution.getImageUrl(),institution.getCatalog())
        print('insert t_institution:[name:%s]'%(institution.getName()) )
        try:
            cur.execute(str)
            conn.commit()
            cur.execute('select @@IDENTITY;')
            last_id = cur.fetchone()[0]
            print(last_id)
            return last_id
        except:
            pass
    def insertPersonevent(self,tableName,personevent,cur,conn):
        str = "INSERT INTO %s(PID,Date,Detail)VALUES('%s','%s','%s')"%(tableName,personevent.getPid(),personevent.getDate(),personevent.getDetail())
        print('insert t_personevent:[PID:%s]'%(personevent.getPid() ))
    
        try:
            cur.execute(str)
            conn.commit()
            cur.execute('select @@IDENTITY;')
            last_id = cur.fetchone()[0]
            print(last_id)
            return last_id
        except:
            raise   
    
    #根据url从person，region，institution表中查询数据
    def selectbyUrl(self,tablename,url,urltype,conn,cur):
        if urltype == 'url':
            str = "select *from %s t where t.URL = '%s'"%(tablename,url)
        elif urltype == 'ImageUrl':
            str = "select *from %s t where t.ImageUrl = '%s'"%(tablename,url)
        result = cur.execute(str)
        if result > 0:
            resultData = cur.fetchone()
            if tablename == 't_person':
                person = Person()
                person.setId(resultData[0])
                person.setName(resultData[1])
                person.setUrl(url)
                person.setImageUrl(resultData[3])
                person.setIntroduction(resultData[4])
                person.setBasicInfo(resultData[5])
                person.setCatalog(resultData[6])
                person.setDetail(resultData[7])
                person.setTag(resultData[8])
                return person
                
            elif tablename == 't_region':
                region = Region()
                region.setId(resultData[0])
                region.setName(resultData[1])
                region.setUrl(resultData[2])
                region.setType(resultData[3])
                region.setTag(resultData[4])
                return region
            elif tablename == 't_institution':
                institution = Institution()
                institution.setId(resultData[0])
                institution.setName(resultData[1])
                institution.setUrl(url)
                institution.setImageUrl(resultData[3])
                institution.setIntroduction(resultData[4])
                institution.setBasicInfo(resultData[5])
                institution.setCatalog(resultData[6])
                institution.setDetail(resultData[7])
                institution.setTag(resultData[8])
                return institution                 
        else: 
            return None
        
    
    
def main():
    p = Parse()
#     p.createConnection()
#     p.parseEntitydata()
    p.parseTaskAData()

if __name__ == '__main__':
    main()