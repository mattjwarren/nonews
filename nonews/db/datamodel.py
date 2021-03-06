'''
Created on 15 Nov 2012

@author: GB108544
'''

from db.components.elements import Schema,Table, Record
from db.components.fields import IntegerField, StringField, RelatedField


class Article(Record):
    def __init__(self):
        self.id=IntegerField(name='id',
                            readable_name='Content ID',
                            size=11,
                            auto_increment=True,
                            default=0,
                            not_null=True,
                            primary_key=True,
                            )

        self.primary_key=(self.id,)

        self.headline=StringField(name='headline',
                                 readable_name="Headline",
                                 size=255,
                                 default="",
                                 not_null=True)
    
        self.body=StringField(name="body",
                             readable_name="Contents",
                             size=8192,
                             default="",
                             not_null=True,
                             unique=True)
    
        unique=(self.body,)

        self.fields=[self.id,self.headline,self.body]    

    def create_sql(self):
        pass

class Articles(Table):
            
    def __init__(self, record_class):
        self.record_class=record_class


                





class Entities(Table):
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

class ArticleEntities(Table):
    
    id=IntegerField(name='id',
                    readable_name='Content ID',
                    size=11,
                    auto_increment=True,
                    default=None,
                    not_null=True,
                    primary_key=True)

    primary_key=id
    
    article_id=RelatedField(name="content_id",
                            readable_name="Content ID",
                            default=None,
                            not_null=True,
                            references=Articles.id)

    entity_id=RelatedField(name="entity_id",
                           readable_name="Entity ID",
                           default=None,
                           not_null=True,
                           references=Entities.id)


    

