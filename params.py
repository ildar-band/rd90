from peewee import *
import sympy
# degree of vertical stability of air
# db_dovsoa = SqliteDatabase('files/dovsoa.db')
from playhouse.reflection import *
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
    k7_f = CharField()  # intorpolite formula

    class Meta:
        database = db

db.connect()
db.create_tables([K1237], safe=True)
# introspector = Introspector.from_database(db)
# models = introspector.generate_models()
#
print(K1237._meta.fields)
# kn = models['k1237']

# for field in K1237._meta.fields:
#     if K1237._meta.fields[field].__class__.__name__ != 'PrimaryKeyField':
#         print(field)
print(K1237.__class__.__name__)
# print([field for field in K1237._meta.fields if K1237._meta.fields[field].__class__.__name__ != 'PrimaryKeyField'])

# print(isinstance(K1237, BaseModel))
def get_peewee_fields(peewee_model):
    if peewee_model.__class__.__name__ == 'BaseModel':
        return [field for field in peewee_model._meta.fields if peewee_model._meta.fields[field].__class__.__name__ != 'PrimaryKeyField']
    else:
        return None
        
# print()
#
# print(get_peewee_fields(K1237))

values = ['Акролеин', 'H2C', None, 0.839, 52.7, 0.2, 0, 0.013, 3, 0.1, 0.2, 0.1, 1, 2.2]
k7 = str(values[-5:])
print(k7)
values = values[:-5]
print(values)
# .append(str(k7))
values.append(k7)
print(values)

k7_list = eval(values[-1])
print(k7_list)

x = sympy.symbols('x')
k7_f = sympy.interpolate(list(zip([-40, -20, 0, 20, 40], k7_list)), x)
values.append(str(k7_f))
print(values)


print(dict(zip(get_peewee_fields(K1237), values)))

# Акролеин (H2C) - 0,839 52,7 0,2 0 0,013 3 0,1 0,2 0,1 1 2,2

# zip(s,t)
# data_source = [
#     {'field1': 'val1-1', 'field2': 'val1-2'},
#     {'field1': 'val2-1', 'field2': 'val2-2'},
#     # ...
# ]

# for data_dict in data_source:
#     Model.create(**data_dict)