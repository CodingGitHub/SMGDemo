'''
Created on 2017年3月30日

@author: lkl51
'''

import requests
# import json
import MySQLdb
from person import Person

#数据解析类
class Parse:
    conn = None
    cur = None
    regionString = None
    organizeString = None
    PTag = None
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

#             yield peopleInfoJson
    
    
    def parseEntitydata(self):
        try:
            f = self.parseDataFromAPI()
            entityInfo = f.__next__()
            while entityInfo:
#                 print(sorted(entityInfo.keys()))
                print(entityInfo)
                self.extractPerson(entityInfo)
                entityInfo = f.__next__()
        except:
            raise
    
    
    def extractPerson(self,entityInfo):
        person = Person()
        
        if 'people_info' in entityInfo:
            people_info = entityInfo['people_info'][0]
            if 'people_tag' in people_info:
                peopleTag = people_info['people_tag']
                person.setTag(peopleTag)
                print(peopleTag)
            if 'people_name' in people_info:
                peoplename = people_info['people_name']
                person.setName(peoplename)
                print(peoplename)
            if '_SON_RELATION' in people_info:
                peopleurl = people_info['_SON_RELATION']['url']
                person.setUrl(peopleurl)
                print(peopleurl)
        
        if 'people_image' in entityInfo:
            people_Image = entityInfo['people_image'][0]
            if 'people_image' in people_Image:
                people_ImageUrl = people_Image['people_image']
                person.setImageUrl(people_ImageUrl)
                print(people_ImageUrl)
            
        if 'introduction' in entityInfo:
            introduction = entityInfo['introduction'][0]
            people_intro = introduction['people_intro']
            person.setIntroduction(people_intro)
            print(people_intro)
        
        if 'people_detail' in entityInfo:
            people_detail = entityInfo['people_detail'][0]
            basic_name = people_detail['basic_name']
            basic_value = people_detail['basic_value']
            
            nameList = basic_name.split('|')
            valueList = basic_value.split('|')
            str = ''
            for i in range(len(nameList)):
                str += nameList[i] + ':' + valueList[i] + ';'            
            print(basic_name,basic_value)
            print(str)
            person.setBasicInfo((str))
            
        if 'catalog' in entityInfo:
            cata = entityInfo['catalog'][0]
            catalog_name = cata['catalog_name']
            person.setCatalog(catalog_name)
            print(catalog_name)
            
        if 'text' in entityInfo:
            text = entityInfo['text'][0]
            text_file = text['text_file']
            person.setDetail(text_file.replace('"',"“"))
            print(text_file)
            
            
        if not self.conn:
            self.createConnection()
            
        dao = Dao()
        dao.insert('t_person', person, self.cur,self.conn)

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