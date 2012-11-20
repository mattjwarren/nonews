'''
Created on 15 Nov 2012

@author: GB108544
'''
from argtools.validation import process_kwargs
#TODO: #from sqltools.emitters import sqlite_emitter

class Field(object):
    def __init__(self,**kwargs):
        process_kwargs(self,
                      #required
                            ["name",],                
                      #with defaults
                            {"readable_name"  :None,
                             "default"        :None,
                             "not_null"       :False,
                             "primary_key"    :False,
                             "unique"         :False,},
                      #keywords
                            kwargs)

    def create_sql(self):
        #TODO: #change to use self.emitter (see from sqltools import in this module)
        pass

class IntegerField(Field):
    def __init__(self,**kwargs):
        Field.__init__(self,**kwargs)
        process_kwargs(self,
                      #required
                            ["size",],
                      #with defaults
                            {"auto_increment" :False,
                            "value" :None,},
                      #keywords
                            kwargs)
        #absoloutes
        self.datatype=int
        
        
class StringField(Field):
    def __init__(self,**kwargs):
        Field.__init__(self,**kwargs)
        process_kwargs(self,
                      #required
                            ["size",],
                      #with defaults
                            False,
                      #keywords
                            kwargs)
                
        self.datatype=str

        def create_sql(self):
            sql ="%s VARCHAR(%d)" % (self.name,self.size)
            sql+=" DEFAULT %s" % self.default   if self.default     else ""
            sql+=" NOT NULL"                    if self.not_null    else ""
            sql+=" PRIMARY KEY"                 if self.primary_key else ""

class relation(object):
    """Represents a db element of type relation"""
    pass

class RelatedField(Field):
    def __init__(self,**kwargs):
        Field.__init__(self,**kwargs)
        process_kwargs(self,
                      #required
                            ["references",],
                      #with defaults
                            False,
                      #keywords
                            kwargs)
        
        self.datatype=relation

class Record(object):
    def __init__(self):
        pass
    
    def create_sql(self):
        pass       
        
        
        
class Table(object):
    def __init__(self,record_class):
        self.record_class=record_class
        
    def create_sql(self):
        pass



    
class Schema(object):
    def __init__(self,tables):
        self.tables=None
    
    def create_sql(self):
        pass
