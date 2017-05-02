from peewee import *
import sympy
# degree of vertical stability of air
# db_dovsoa = SqliteDatabase('files/dovsoa.db')
from playhouse.reflection import *
import re
from xlsxing import list_from_xlsx

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


# introspector = Introspector.from_database(db)
# models = introspector.generate_models()
#

# kn = models['k1237']

# for field in K1237._meta.fields:
#     if K1237._meta.fields[field].__class__.__name__ != 'PrimaryKeyField':
#         print(field)

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
#     print(values)
    print(values[0])
    hcs = re.search(r'([a-яА-ЯёЁ ]*\(?[a-яА-ЯёЁ ]+\)?)\s*([A-Za-z0-9()]*)', values[0])

    values[0] = hcs.group(1).strip() if hcs.group(1) else values[0]
    values.insert(1, hcs.group(2).strip()) if hcs.group(2) else values.insert(1, '')


    k7_1 = [] # для первичного облака
    k7_2 = [] # для вторичного облака
    k7 = values[-5:]
    values = values[:-5]
    for key_val, val in enumerate(values):
        if key_val >= 2:
            values[key_val] = float(values[key_val]) if values[key_val] else None

    print(values)

    for i in k7:
        k7_re = re.search(r'([0-9.-]+)\s*([0-9.]*)', i)
        # print(k7_re.group(2))
        k7_1.append(float(k7_re.group(1))) if k7_re.group(1) else k7_1.append(None)
        if k7_re.group(2):
            k7_2.append(float(k7_re.group(2)))
        else:
            k7_2 = None

       # k7_1 = [re.search(r'([0-9.]+)\s+([0-9.]+)', k7_1).group(1) for k7_1 in k7 if re.search(r'([0-9.]+)\s+([0-9.]+)', k7_1)]
# k7_2 = [re.search(r'([0-9.]+)\s+([0-9.]+)', k7_1).group(2) for k7_1 in k7 if re.search(r'([0-9.]+)\s+([0-9.]+)', k7_1)]

    print('k7_1: %s' % k7_1)
    print('k7_2: %s' % k7_2)

    values.append(str(k7_1))
    x = sympy.symbols('x')
    k7_1_f = sympy.interpolate(list(zip([-40, -20, 0, 20, 40], k7_1)), x)
    values.append(str(k7_1_f))
    # print(values)



    x = sympy.symbols('x')
    if k7_2:
        values.append(str(k7_2))
        k7_2_f = sympy.interpolate(list(zip([-40, -20, 0, 20, 40], k7_2)), x)
        values.append(str(k7_2_f))
    else:
        k7_2, k7_2_f = None, None
        values.append(k7_2)
        values.append(k7_2_f)

    print(values)

    return dict(zip(get_peewee_fields(K1237), values))

# aaaa = ['Аммиак хранение под давлением (NH3)', '0.0008', '0.681', '-33.42', '15', '0.18', '0.025', '0.04', '0 0.9', '01 1',
#      '06 1', '1 1', '14 1']
# bbb = ['Акролеин (H2C)', '-', '0.839', '52.7', '0.2', '0', '0.013', '3', '0.1', '0.2', '0.1', '1', '2.2']



# Акролеин (H2C) - 0,839 52,7 0,2 0 0,013 3 0,1 0,2 0,1 1 2,2

# zip(s,t)
# data_source = [
#     {'field1': 'val1-1', 'field2': 'val1-2'},
#     {'field1': 'val2-1', 'field2': 'val2-2'},
#     # ...
# ]

# for data_dict in data_source:
#     Model.create(**data_dict)

if __name__ == '__main__':

    db.create_tables([K1237], safe=True)
    print(K1237._meta.fields)
    print(K1237.__class__.__name__)
    params_list = list_from_xlsx('files/tab p2.xlsx')
    params_source = [get_str_K1237(row) for row in params_list]
    print(params_source)
    aa = {'hcs_name': 'Этилмеркаптан', 'hcs_form': '(C2H5SH)', 'gas_density': None, 'liquid_density': 0.839, 'boiling_t': 35.0, 'toxodeth': 2.2, 'k1': 0.0, 'k2': 0.028, 'k3': 0.27, 'k7_1': '[0.1, 0.2, 0.5, 1.0, 1.7]', 'k7_1_f': '-1.85288457211878e-22*x**4 - 1.6940658945086e-21*x**3 + 0.00025*x**2 + 0.02*x + 0.5', 'k7_2': None, 'k7_2_f': None}
    # get_str_K1237(aaaa)
    # data_source = [aa]
    with db.atomic():
        K1237.insert_many(params_source).execute()

    # for data_dict in data_source:
    #     print(data_dict)
    #     K1237.create(**data_dict)