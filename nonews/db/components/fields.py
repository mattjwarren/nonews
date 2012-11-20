'''
Created on 20 Nov 2012

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
        if self.default:
            self.value=self.default
        else:
            self.value=None

    def create_sql(self):
        #TODO: #change to use self.emitter (see from sqltools import in this module)
        pass
    
    def validate(self,value):
        """return true if value is valid type for this field"""
        return type(value) is self.datatype

class IntegerField(Field):
    def __init__(self,**kwargs):
        Field.__init__(self,**kwargs)
        process_kwargs(self,
                      #required
                            ["size",],
                      #with defaults
                            {"auto_increment" :False,},
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
        
    def validate(self,value):
        return type(value) is int #Need to figure this out!
                    #check the value points
                    #to a valid record of the type referenced
                    #.. or is just an int? (for now..)
                    
                    