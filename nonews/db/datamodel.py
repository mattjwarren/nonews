'''
Created on 15 Nov 2012

@author: GB108544
'''

from db_elements import Schema,Table
from db_elements import IntegerField, StringField




class Content(Table):
    id=IntegerField(name='id',
                    readable_name='Content ID',
                    size=11,
                    auto_increment=True,
                    default=None,
                    not_null=True)
    
    headline=StringField(name='headline',
                         readable_name="Headline",
                         size=255,
                         default=None,
                         not_null=True)
    
    body=StringField(name="body",
                     readable_name="Contents",
                     size=8192,
                     default=None,
                     not_null=True)


class Entity(Table):
    id=IntegerField(name='id',
                    readable_name='Content ID',
                    size=11,
                    auto_increment=True,
                    default=None,
                    not_null=True)
    
    name=StringField(name="name",
                     readable_name="Name",
                     size=128,
                     default=None,
                     not_null=True)

class ContentEntities(Table):
    
    id=IntegerField(name='id',
                    readable_name='Content ID',
                    size=11,
                    auto_increment=True,
                    default=None,
                    not_null=True)

    primary_key=id
    
    content_id=RelatedField(name="content_id",
                            readable_name="Content ID",
                            default=None,
                            not_null=True,
                            related_to=Content.id)

    entity_id=RelatedField(name="entity_id",
                           readable_name="Entity ID",
                           default=None,
                           not_null=True,
                           related_to=Entity.id)


    

