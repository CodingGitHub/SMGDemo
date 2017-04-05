'''
Created on 2017年4月5日

@author: Deng
'''
class Relation:
    id = None
    id1 = None
    id2 =  None
    type = None
    name = None
    strength = None
    
    def setId(self,i):
        self.id = i
    def getId(self):
        return self.id
    
    def setId1(self,i1):
        self.id1 = i1
    def getId1(self):
        return self.id1
    
    def setId2(self,i2):
        self.id2 = i2
    def getId2(self):
        return self.id2
    
    def setType(self,type):
        self.type = type
    def getType(self):
        return self.type
    
    def setName(self,name):
        self.name = name
    def getName(self):
        return self.name
    
    def setStrength(self,strength):
        self.strength = strength
    def getStrength(self):
        return self.strength
    