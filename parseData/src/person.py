'''
Created on 2017年3月31日

@author: lkl51
'''
class Person:
    id = None
    name = None
    url = None
    introduction = None
    basicinfo = None
    detail = None
    catalog = None
    tag = None
    imageUrl = None
    
    def setId(self,i):
        self.id = i
    def getId(self):
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
    
    def setCatalog(self,clog):
        self.catalog = clog
    def getCatalog(self):
        return self.catalog
    
    def setTag(self,ta):
        self.tag = ta
    def getTag(self):
        return self.tag
    
    def setImageUrl(self,url):
        self.imageUrl = url
    def getImageUrl(self):
        return self.imageUrl
    
    def setDetail(self,det):
        self.detail = det
    def getDetail(self):
        return self.detail
    
    
    
    
    