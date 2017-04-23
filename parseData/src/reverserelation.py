'''
Created on 2017年4月16日

@author: Deng
'''
import MySQLdb

class ReverseRelation:
    
    conn = None
    cur = None
    #def createConnection(self,host='120.27.27.83',user='media_demo_user',passwd='6yhnMJU&',db='media_demo',port=20002):
    def createConnection(self,host='localhost',user='root',passwd='sh931023',db='media_demo',port=3306):
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
        dao = Dao()
        if not self.conn:
            self.createConnection()
        reverseRelationAll = dao.selectDataAll('t_relation', self.conn, self.cur)
        for reverseRelation in reverseRelationAll:
            #print(reverseRelation)
            id = reverseRelation[0]
            id1 = reverseRelation[1]
            id2 = reverseRelation[2]
            type = reverseRelation[3]
            #Name,RelationDescribe,Prtype,Strength
            name = reverseRelation[4]
            relationdescribe = reverseRelation[5]
            prtype = reverseRelation[6]
            strength = reverseRelation[7]
            
            if type == '1':
                if dao.selectData(self.conn, self.cur, id1, id2):
                    continue
                else:
                    dao.insertData(id1,id2,type,name,relationdescribe,prtype,strength,self.conn,self.cur)
        self.conn.commit()

class Dao:
    def selectDataAll(self,tablename,conn,cur):
        if tablename == 't_relation':
            str = 'select * from %s t' % tablename
            print(cur.execute(str))
            return (cur.fetchall())
    
    def selectData(self,conn,cur,id1,id2):
        str = 'select * from t_relation t where t.id1 = %s and t.id2 = %s'%(id2,id1)
        print(cur.execute(str))
        return (cur.fetchall())
    
    def insertData(self,id1,id2,type,name,relationdescribe,prtype,strength,conn,cur):
        str =  "INSERT INTO t_relation (ID1,ID2,Type,Name,RelationDescribe,Prtype,Strength) VALUES('%s','%s','%s','%s','%s','%s','%s')"%(id2,id1,type,name,relationdescribe,prtype,strength)
        print(str)
        print(cur.execute(str))

            
            
def main():
    p = ReverseRelation()
    p.reverse()

if __name__ == '__main__':
    main()         
            
            