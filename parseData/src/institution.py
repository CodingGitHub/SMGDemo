'''
Created on 2017年3月31日

@author: Deng
'''
class Institution:
    id = None
    name = None
    url = None
    introduction = None
    basicinfo = None
    detail = None
    reference = None
    tag = None
    def setId(self,i):
        self.id = i
    def getid(self):
        return self.id
    
    def setName(self,name):
        self.name = name
    def getName(self):
        return self.name
    
    def setUrl(self,url):
        self.url = url
    def getUrl(self):
        return self.url
    
    def setIntroduction(self,intro):
        self.introduction = intro
    def getIntroduction(self):
        return self.introduction
    
    def setBasicInfo(self,bsinfo):
        self.basicinfo = bsinfo
    def getBasicInfo(self):
        return self.basicinfo
    def setDetail(self,detail):
        self.detail = detail
    def getDetail(self):
        return self.detail
    def setReference(self,refer):
        self.reference = refer
    def getReference(self):
        return self.reference
    def setTag(self,tag):
        self.tag = tag
    def getTag(self):
        return self.tag
        