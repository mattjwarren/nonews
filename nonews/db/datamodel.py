'''
Created on 15 Nov 2012

@author: GB108544
'''

from db_elements import Schema,Table
from db_elements import IntegerField, StringField, RelatedField




class Content(Table):
    id=IntegerField(name='id',
                    readable_name='Content ID',
                    size=11,
                    auto_increment=True,
                    default=None,
                    not_null=True,
                    primary_key=True)

    primary_key=id
    
    headline=StringField(name='headline',
                         readable_name="Headline",
                         size=255,
                         default=None,
                         not_null=True)
    
    body=StringField(name="body",
                     readable_name="Contents",
                     size=8192,
                     default=None,
                     not_null=True,
                     unique=True)
    
    unique=(body,)

class Entity(Table):
    id=IntegerField(name='id',
                    readable_name='Content ID',
                    size=11,
                    auto_increment=True,
                    default=None,
                    not_null=True,
                    primary_key=True)

    primary_key=id
    
    name=StringField(name="name",
                     readable_name="Name",
                     size=128,
                     default=None,
                     not_null=True,
                     unique=True)

    unique=(name,)

class ContentEntities(Table):
    
    id=IntegerField(name='id',
                    readable_name='Content ID',
                    size=11,
                    auto_increment=True,
                    default=None,
                    not_null=True,
                    primary_key=True)

    primary_key=id
    
    content_id=RelatedField(name="content_id",
                            readable_name="Content ID",
                            default=None,
                            not_null=True,
                            references=Content.id)

    entity_id=RelatedField(name="entity_id",
                           readable_name="Entity ID",
                           default=None,
                           not_null=True,
                           references=Entity.id)


    

