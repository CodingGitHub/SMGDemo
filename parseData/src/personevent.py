'''
Created on 2017年4月5日

@author: Deng
'''
class PersonEvent:
    id = None
    pid = None
    date = None
    detail = None
    
    def setId(self,i):
        self.id = i
    def getId(self):
        return self.id
    
    def setPid(self,pid):
        self.pid = pid
    def getPid(self):
        return self.pid
    
    def setDate(self,date):
        self.date = date
    def getDate(self):
        return self.date
    
    def setDetail(self,detail):
        self.detail = detail
    def getDetail(self):
        return self.detail
    
    
    