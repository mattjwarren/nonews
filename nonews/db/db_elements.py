'''
Created on 15 Nov 2012

@author: GB108544
'''

class Field(object):
    def __init__(self,**kwargs):        
        try:
            self.name=kwargs["name"]
        except KeyError:
            raise Exception("Required keyword parameter 'name' not found.")
        
        try:        
            self.readable_name=kwargs["readable_name"]
        except KeyError:
            self.readable_name=None
        
        try:
            self.default=kwargs["default"]
        except KeyError:
            self.default=None
        
        try:
            self.not_null=kwargs["not_null"]
        except KeyError:
            self.not_null=False

    def create_sql(self):
        pass

class IntegerField(Field):
    def __init__(self,**kwargs):
        Field.__init__(self,kwargs)
        self.datatype=int
        try:
            self.auto_increment=kwargs["auto_increment"]
        except KeyError:
            self.auto_increment=False
        try:
            self.size=kwargs["size"]
        except KeyError:
            raise Exception("IntegerField requires 'size' parameter.")

class StringField(Field):
    def __init__(self,**kwargs):
        Field.__init__(self,kwargs)
        self.datatype=str
        try:
            self.size=kwargs["size"]
        except KeyError:
            raise Exception("StringField requires 'size' parameter.")
        
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
