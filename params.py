from peewee import *

# degree of vertical stability of air
# db_dovsoa = SqliteDatabase('files/dovsoa.db')

db = SqliteDatabase('files/k1237.db')

class K1237(Model):
    hcs_name = CharField() # hazardous chemical substance
    hcs_form = CharField()
    gas_density = FloatField()
    liquid_density = FloatField()
    boiling_t = FloatField()
    toxodeth = FloatField()
    k1 = FloatField()
    k2 = FloatField()
    k3 = FloatField()
    k7 = CharField() #  '[0.1, 0.2, 0.1, 1, 2.2]'

    class Meta:
        database = db


db.connect()
db.create_tables(['K1237'])
data_source = [
    {'field1': 'val1-1', 'field2': 'val1-2'},
    {'field1': 'val2-1', 'field2': 'val2-2'},
    # ...
]

for data_dict in data_source:
    Model.create(**data_dict)