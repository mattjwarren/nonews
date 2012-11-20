'''
Created on 16 Nov 2012

@author: matt
'''

def rows_to_records(rows,record_class):
        
    records=[]
    
    for row in rows:
        new_record=record_class()
        [ setattr(new_record.field,"value",row[idx])
            for idx,field in enumerate(new_record.fields)
                if field.validate(row[idx]) ]
        records.append(new_record)
    return records
    
    
    