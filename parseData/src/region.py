'''
Created on 2017年3月31日

@author: Deng
'''
class Region:
    id = None
    name = None
    url = None
    type = None
    tag = None
    
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
    def setType(self,ty):
        self.type = ty
    def getType(self):
        return self.type
    def setTag(self,tag):
        self.tag = tag
    def getTag(self):
        return self.tag