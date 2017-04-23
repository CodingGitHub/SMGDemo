'''
Created on 2017年4月14日

@author: lkl51

'''
import MySQLdb
import re


class Parse:
    
    conn = None
    cur = None
    relationdict = {}
    relationtypedict = {}
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
            
        #分割全文（By句）
    def cutText(self,text_file):
        if  not isinstance(text_file,str): #判断是否为str类型
            text_file = str(text_file)
        puzs = frozenset('。！？,.!?，') #划分标志结合
        tmp = []
        for ch in text_file: #遍历全文
            tmp.append(ch)
            if puzs.__contains__(ch):#判断是否为断句标志
                yield ''.join(tmp)
                tmp = []
        yield ''.join(tmp)
        
    #判断关系名称                 
    def judgeRelation(self,secondName,cutText):
        if not self.relationdict:
            self.readRelationdict()
        if cutText:
            for subject in cutText:   #遍历文章中的每个句子
                if re.search(secondName,subject): #判断实体名字是否在句子中
                    key = self.isKeyInSubject(subject)
                    if not key == '':
                        return self.relationdict[key],subject #返回关系名称、关系描述
                    else:
                        return None,subject
        return None,None
    
    def isKeyInSubject(self,subject):
        keyword = ''
        for key in self.relationdict.keys():
            if key in subject:
                keyword = key
                break;
        return keyword
    
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
                
            
    def parse(self):
        dao = Dao()
        if not self.conn:
            self.createConnection()
#         dao.selectData('t_person', 1, self.conn, self.cur)
        relationAll = dao.selectData('t_relation',1,self.conn,self.cur,None)
        for relation in relationAll:
            print(relation)
            id = relation[0]
            id1 = relation[1]
            id2 = relation[2]
            person1Detail = dao.selectData('t_person', id1, self.conn, self.cur,'Detail')
            person2Name = dao.selectData('t_person', id2, self.conn, self.cur,'Name')
            relationName,relationDes = self.judgeRelation(person2Name, self.cutText(person1Detail))
            if relationDes:
                relationDes = relationDes.replace("'","''").replace("\\","")
            relationPrType = self.judgeRelationType(relationName)
            str = "update t_relation t set t.Name = '%s',t.RelationDescribe = '%s',t.prType = '%s' where t.ID = %s"%(relationName,relationDes,relationPrType,id)
            print(str)
            self.cur.execute(str)
        self.conn.commit()
    
    
            
class Dao:
    def selectData(self,tablename,id,conn,cur,attr):
        if tablename == 't_person':
            if attr == 'Detail':
                str = 'select t.Detail from %s t where t.id = %d'%(tablename,id)
                print(cur.execute(str))
                return cur.fetchone()[0]
            elif attr == 'Name':
                str = 'select t.Name from %s t where t.id = %d'%(tablename,id)
                print(cur.execute(str))
                return cur.fetchone()[0]
            
        if tablename == 't_relation':
            str = 'select t.ID,t.ID1,t.ID2 from %s t where t.Type = 1' % tablename
            print(cur.execute(str))
            return (cur.fetchall())
        



def main():
    parse = Parse()
    parse.parse()

if __name__ == '__main__':
    main()