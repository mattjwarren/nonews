'''
Created on 16 Nov 2012

@author: matt
'''
from db_elements import Record

def rows_to_objects(data,klass=Table):
    """data=[[row],[row],...]"""
    headers,rows=data
    
    instances=[]
    
    for row in rows:
        klass_attrs=dict(zip(headers,row))
        new_instance=klass(fields=klass.fields,**klass_attrs)
        instances.append(new_instance)
        
    return instances
    
    
    