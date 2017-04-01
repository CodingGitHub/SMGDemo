'''
Created on 2017年3月30日

@author: lkl51
'''


import requests
import json
import MySQLdb
from person import Person


class Parse:
    conn = None
    cur = None
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
        
    #调用API得到的数据，并解析数据得到data的value下 的data_json的value    
    def parseDataFromAPI(self,key=None,task_id=None,task_period=None,data_name=None,pgfrom=None,pgsize=None):
        url = "http://120.27.27.83:8081/api/data/getspiderconsolidateddata?key=&task_id=1490862367&task_period=20170331_0942&data_name=&pgfrom=1&pgsize=30"
        page = requests.get(url)
        jsn = page.json()
#         print(jsn)
#         print(jsn.keys())
#         print(jsn['data'])
        for d in jsn['data']:
#             print(d['data_json'])
            peopleInfoJson = eval(d['data_json'])
#             print(peopleInfoJson.keys())
#             with open('people.txt','a+',encoding = 'utf-8') as f:
#                 for key in peopleInfoJson.keys():
#                     f.write(key + ':')
#                     f.write('\t')
#                     f.write(str(peopleInfoJson[key]) + '\n')
#                 f.write('\n\n\n\n')
            yield peopleInfoJson
    
    
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
            
    
    
    #1:人物；2：地域；3：机构    
    def getEntityType(self,entityName,entityTag):
        pass



class Dao():
    def insert(self,tableName,person,cur,conn):
        str = 'INSERT INTO %s(Name,URL,Introduction,BasicInfo,Catalog,Reference,Tag,ImageUrl,Detail) VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s")'%(tableName,person.getName(),person.getUrl(),person.getIntroduction(),person.getBasicInfo(),person.getCatalog(),person.getReference(),person.getTag(),person.getImageUrl(),person.getDetail())
        print(str)
        print(cur.execute(str))
        conn.commit()
        return cur.execute('select @@IDENTITY;')            
    
def main():
    p = Parse()
#     p.createConnection()
    p.parseEntitydata()
#     p.parseDataFromAPI()

if __name__ == '__main__':
    main()