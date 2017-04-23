'''
Created on 2017年4月17日

@author: lkl51
'''
import MySQLdb
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



class Remove:
    
    conn = None
    cur = None
    imageUrlSet = set()
    insImageUrlSet = set()
    relationlist = []
    def createConnection(self,host='120.27.27.83',user='media_demo_user',passwd='6yhnMJU&',db='media_demo',port=20002):
#     def createConnection(self,host='localhost',user='root',passwd='sh931023',db='media_demo',port=3306):
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
    
    def reverse(self):
        self.dao = Dao()
        if not self.conn:
            self.createConnection()
            
        personAll = self.dao.selectDataAll('t_person', self.conn, self.cur)
        for person in personAll:
            imageUrl = person[3]
            if imageUrl:
                if imageUrl not in self.imageUrlSet:
                    self.imageUrlSet.add(imageUrl)
                else:
                
                    savedPerson = self.isInDatabase(url = None, ImageUrl = imageUrl, type = 1)[1]
                    if savedPerson:
#                         print(person[0])
#                         print(savedPerson.getId())
                        oldID = person[0]
                        newID = savedPerson.getId()                   
                        
                        self.dao.updateDataById1(newID,oldID, self.conn, self.cur)
                        self.dao.updateDataById2(newID,oldID, 1,self.conn, self.cur)
                        self.dao.deletePerson('t_person', person[0],self.conn, self.cur)
                        
        
        institutionAll = self.dao.selectDataAll('t_institution', self.conn, self.cur)
        for ins in institutionAll:
            imageUrl = ins[3]
            if imageUrl:
                if imageUrl not in self.insImageUrlSet:
                    self.insImageUrlSet.add(imageUrl)
                else:
                
                    savedInstitution = self.isInDatabase(url = None, ImageUrl = imageUrl, type = 3)[1]
                    if savedInstitution:
#                         print(person[0])
#                         print(savedPerson.getId())
                        oldID = ins[0]
                        newID = savedInstitution.getId()                   
                        
#                         self.dao.updateDataById1(newID,oldID, self.conn, self.cur)
                        self.dao.updateDataById2(newID,oldID,3, self.conn, self.cur)
                        self.dao.deletePerson('t_institution', ins[0],self.conn, self.cur)
                    
                            
#         reverseRelationAll = dao.selectDataAll('t_relation', self.conn, self.cur)
#         for reverseRelation in reverseRelationAll:
#             #print(reverseRelation)
#             id = reverseRelation[0]
#             id1 = reverseRelation[1]
#             id2 = reverseRelation[2]
#             type = reverseRelation[3]
#             #Name,RelationDescribe,Prtype,Strength
#             name = reverseRelation[4]
#             relationdescribe = reverseRelation[5]
#             prtype = reverseRelation[6]
#             strength = reverseRelation[7]
#             
#             if type == '1':
#                 if dao.selectData(self.conn, self.cur, id1, id2):
#                     continue
#                 else:
#                     dao.insertData(id1,id2,type,name,relationdescribe,prtype,strength,self.conn,self.cur)
        self.conn.commit()
        
    
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
    
    
    def removeRelation(self):
        relations = self.dao.selectDataAll('t_relation',self.conn,self.cur)
        for relation in relations:
            id1 = relation[1]
            id2 = relation[2]
            type = relation[3]
            tup = (id1,id2,type)
            if tup not in self.relationlist:
                self.relationlist.append(tup)
            else :
                self.dao.deleterelation(relation[0], self.conn, self.cur)
        
class Dao:
    def selectDataAll(self,tablename,conn,cur):
#         if tablename == 't_relation':
        str = 'select * from %s t ' % tablename
        print(cur.execute(str))
        return (cur.fetchall())
    
    def selectData(self,conn,cur,id1,id2):
        str = 'select * from t_relation t where t.id1 = %s and t.id2 = %s'%(id1,id2)
        if (cur.execute(str)) > 0:
            return True
        else :
            return False
    
    def insertData(self,id1,id2,type,name,relationdescribe,prtype,strength,conn,cur):
        str =  "INSERT INTO t_relation (ID1,ID2,Type,Name,RelationDescribe,Prtype,Strength) VALUES('%s','%s','%s','%s','%s','%s','%s')"%(id2,id1,type,name,relationdescribe,prtype,strength)
        print(str)
        print(cur.execute(str))
        
    #根据url从person，region，institution表中查询数据
    def selectbyUrl(self,tablename,url,urltype,conn,cur):
        if urltype == 'url':
            str = "select *from %s t where t.URL = '%s'"%(tablename,url)
        elif urltype == 'ImageUrl':
            str = "select *from %s t where t.ImageUrl = '%s'"%(tablename,url)
        result = cur.execute(str)
        if result > 1:
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
        
        
    def updateDataById1(self,newID1,oldID1,conn,cur):
        str = 'update t_relation t set t.ID1 = %d where t.ID1 = %d '% (newID1,oldID1)
        print(str)
        cur.execute(str)
        conn.commit()
        
    def updateDataById2(self,newID2,oldID2,type,conn,cur):
        str = 'update t_relation t set t.ID2 = %d where t.ID2 = %d and t.Type = %d ' % (newID2,oldID2,type)
        print(str)
        cur.execute(str)
        
        conn.commit()
    def deletePerson(self,tablename,id,conn,cur):
        str = 'DELETE FROM %s WHERE ID = %s' %(tablename, id)
        cur.execute(str)
        conn.commit()
        
    def deleterelation(self,id,conn,cur):
        str = 'DELETE FROM t_relation WHERE ID = %s' % id
        cur.execute(str)
        conn.commit()
        
def main():
    p = Remove()
#     p.reverse()
    p.removeRelation()

if __name__ == '__main__':
    main() 
            