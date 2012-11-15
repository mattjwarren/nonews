'''
Created on 15 Nov 2012

@author: GB108544
'''

class Datatype(object):
    """Subclass to represent a SQL datatype"""
    pass

class Integer(Datatype):
    pass

class String(Datatype):
    pass

class Field(object):
    def __init__(self,
                 name           =None,
                 readable_name  =None,
                 datatype       =None,
                 size           =None):
        
        self.name=name
        self.readable_name=readable_name
        self.datatype=datatype
        self.size=size

    def create_sql(self):
        pass
    
class Table(object):
    def __init__(self,fields=None):
        self.fields=fields
        
    def create_sql(self):
        pass
    
class Schema(object):
    def __init__(self,tables):
        self.tables=None
    
    def create_sql(self):
        pass
