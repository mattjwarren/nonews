'''
Created on 16 Nov 2012

@author: GB108544
'''
from argtools.validation import process_kwargs
import sqlite3

class sqlite_connection(object):
    def __init__(self,**kwargs):
        process_kwargs(self,
                       #required
                       ["database_name"],
                       #with defaults
                       None,
                       #keywords
                       kwargs)
        try:
            self.connection=sqlite3.connect(self.database_name)
            self.cursor=self.connection.cursor()
        except sqlite3.Error, e:
            raise Exception( "Problem creating connection and getting cursor: %s" % e.args[0] )
        
        def execute(self,sql):
            try:
                self.cursor.execute(sql)
            except sqlite3.Error, e:
                raise Exception( "Problem executing SQL: %s" % e.args[0] )
            
            return self.cursor.fetchall()