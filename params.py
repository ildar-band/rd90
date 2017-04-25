from peewee import *
import sympy
# degree of vertical stability of air
# db_dovsoa = SqliteDatabase('files/dovsoa.db')
from playhouse.reflection import *
import re

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
    k7_1 = CharField() #  '[0.1, 0.2, 0.1, 1, 2.2]'  - первичное облако
    k7_1_f = CharField() # intorpolite formula
    k7_2 = CharField() #  '[0.1, 0.2, 0.1, 1, 2.2]'  - вторичное облако
    k7_2_f = CharField()  # intorpolite formula

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

def get_str_K1237(params_line_from_file):
    values = params_line_from_file
# ['Аммиак хранение под давлением (NH3)', '0.0008', '0.681', '-33.42', '15', '0.18', '0.025', '0.04', '0 0.9',	'01 1', '06 1',	'1 1',	'14 1']
    print(values)
    hcs = re.search(r'([a-яА-ЯёЁ ()]*)\s*\(([A-Z0-9()]*)\)', values[0])
    print(hcs.group(2))
    values[0] = hcs.group(1).strip()
    values.insert(1, hcs.group(2).strip())
# values = values[0]+
# val
# values =
    print(values)

    k7_1 = [] # для первичного облака
    k7_2 = [] # для вторичного облака
    k7 = values[-5:]

# k7 = ['0 0.9', '01 1', '06 1', '1 1', '14 1']

    for i in k7:
        k7_re = re.search(r'([0-9.]+)\s+([0-9.]+)', i)
        if k7_re:
            k7_1.append(float(k7_re.group(1)))
            k7_2.append(float(k7_re.group(2)))
#
# k7_1 = [re.search(r'([0-9.]+)\s+([0-9.]+)', k7_1).group(1) for k7_1 in k7 if re.search(r'([0-9.]+)\s+([0-9.]+)', k7_1)]
# k7_2 = [re.search(r'([0-9.]+)\s+([0-9.]+)', k7_1).group(2) for k7_1 in k7 if re.search(r'([0-9.]+)\s+([0-9.]+)', k7_1)]
    print('k7_1: %s' % k7_1)
    print('k7_2: %s' % k7_2)
    # k7 = str(values[-5:])
    # print(k7)
    values = values[:-5]
    print(values)
    # .append(str(k7))
    values.append(str(k7_1))
    values.append(str(k7_2))
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