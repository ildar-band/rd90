from peewee import *

db = SqliteDatabase('files/k1237.db')
db.connect()


class K1237(Model):
    hcs_name = CharField() # hazardous chemical substance
    hcs_form = CharField()
    gas_density = FloatField(null=True)
    liquid_density = FloatField(null=True)
    boiling_t = FloatField(null=True)
    toxodeth = FloatField(null=True)
    k1 = FloatField(null=True)
    k2 = FloatField(null=True)
    k3 = FloatField(null=True)
    k7_1 = CharField(null=True) #  '[0.1, 0.2, 0.1, 1, 2.2]'  - первичное облако
    k7_1_f = CharField(null=True) # intorpolite formula
    k7_2 = CharField(null=True) #  '[0.1, 0.2, 0.1, 1, 2.2]'  - вторичное облако
    k7_2_f = CharField(null=True)  # intorpolite formula

    class Meta:
        database = db


def get_peewee_fields(peewee_model):
    if peewee_model.__class__.__name__ == 'BaseModel':
        return [field for field in peewee_model._meta.fields if peewee_model._meta.fields[field].__class__.__name__ != 'PrimaryKeyField']
    else:
        return None