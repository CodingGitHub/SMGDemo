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
    catalog = None
    detail = None
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
    def setDetail(self,detail):
        self.detail = detail
    def getDetail(self):
        return self.detail
    
    def setTag(self,tag):
        self.tag = tag
    def getTag(self):
        return self.tag
    def setImageUrl(self,url):
        self.imageUrl = url
    def getImageUrl(self):
        return self.imageUrl
    
    def setCatalog(self,cata):
        self.catalog = cata
    def getCatalog(self):
        return self.catalog