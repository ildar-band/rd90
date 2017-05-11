import sympy
# degree of vertical stability of air
# db_dovsoa = SqliteDatabase('files/dovsoa.db')
from playhouse.reflection import *
import re

import math
import k1237


def get_k1(k1237):
    # К1 - коэффициент, зависящий от условий хранения АХОВ, для сжатых газов К1 = 1
    # Значения К1 для изотермического хранения аммиака приведено для случая разлива (выброса) в поддон.
    return 1 if k1237.gas_density else k1237.k1


def get_substance_mount(substance_mount, k1237):
    # При авариях на хранилищах сжатого газа - substance_mount - это объем хранилища
    # При авариях на хранилищах сжатого газа Q0 рассчитывается по формуле Q0 = d*Vх
    return substance_mount * k1237.gas_density if k1237.gas_density else substance_mount


def get_k3(hcs_id, K1237):
    # коэффициент, равный отношению пороговой токсодозы хлора к пороговой токсодозе другого АХОВ
    k3 = K1237.get(K1237.hcs_id == hcs_id).k3
    return k3


k4_list = list(zip([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15], [1, 1.33, 1.67, 2.0, 2.34, 2.67, 3.0, 3.34, 3.67, 4.0, 5.68]))
interpol_k4_func = sympy.interpolate(k4_list, x)

def get_k4(wind_speed, func):
    x = (math.ceil(wind_speed))
    # interpol_k4_func = sympy.interpolate(k4_list, x)
    # k4 = [1, 1.33, 1.67, 2.0, 2.34, 2.67, 3.0, 3.34, 3.67, 4.0, 5.68]
    return k4[i-1]


def get_k5(dovsoa):
    # коэффициент, учитывающий степень вертикальной устойчивости воздуха
    if dovsoa == 'ин':
        return 1
    if dovsoa == 'из':
        return 0.23
    if dovsoa == 'к':
        return 0.08


# коэффициент, учитывающий влияние температуры воздуха ; для сжатых газов К7 = 1;
def get_k7(k1237, air_t, cloud =1):
    # value_list = list(zip([-40, -20, 0, 20, 40], eval(val_list)))
    x = float(air_t)
    if cloud == 1:
        # print(k1237.k7_1_f)
        k7 = eval(k1237.k7_1_f)
    elif cloud == 2:
        k7 = eval(k1237.k7_1_f)
    else:
       return None
    return k7


def get_density(atmospheric_pressure=1):
    # Плотности газообразных СДЯВ gas_density приведены для атмосферного давления; при давлении в емкости,
    # отличном от атмосферного, плотности определяются путем умножения данных графы 3 на значение
    # давления в атмосферах (1 атм = 760 мм рт. ст.).
    pass


def get_k1(hcs_id, K1237, hcs_storage='no_pressure'):
    # hcs - hazardous chemical substance
    # hcs_storage - 'gas_under_pressure' || 'no_pressure'
    # К1 - коэффициент, зависящий от условий хранения АХОВ, для сжатых газов К1 = 1
    # Значения К1 для изотермического хранения аммиака приведено для случая разлива (выброса) в поддон.
    # для сжатых газов К1 = 1
    k1 = K1237.get(K1237.hcs_id == hcs_id).k1
    if hcs_storage == 'gas_under_pressure':
        k1 = 1
    return k1

def get_k3(hcs_id, K1237):
    # коэффициент, равный отношению пороговой токсодозы хлора к пороговой токсодозе другого АХОВ
    k3 = K1237.get(K1237.hcs_id == hcs_id).k3
    return k3


def get_k4(wind_speed):
    i = (math.ceil(wind_speed))
    k4 = [1, 1.33, 1.67, 2.0, 2.34, 2.67, 3.0, 3.34, 3.67, 4.0, 5.68]
    return k4[i-1]


def get_k5(dovsoa):
    # коэффициент, учитывающий степень вертикальной устойчивости воздуха
    if dovsoa == 'ин':
        return 1
    if dovsoa == 'и3':
        return 0.23
    if dovsoa == 'к':
        return 0.08


def get_density(atmospheric_pressure=1):
    # Плотности газообразных СДЯВ gas_density приведены для атмосферного давления; при давлении в емкости,
    # отличном от атмосферного, плотности определяются путем умножения данных графы 3 на значение
    # давления в атмосферах (1 атм = 760 мм рт. ст.).
    pass





# introspector = Introspector.from_database(db)
# models = introspector.generate_models()
#

# kn = models['k1237']

# for field in K1237._meta.fields:
#     if K1237._meta.fields[field].__class__.__name__ != 'PrimaryKeyField':
#         print(field)

# print([field for field in K1237._meta.fields if K1237._meta.fields[field].__class__.__name__ != 'PrimaryKeyField'])

# print(isinstance(K1237, BaseModel))

        
# print()
#
# print(get_peewee_fields(K1237))








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

    # db.create_tables([K1237], safe=True)
    print(K1237._meta.fields)
    print(K1237.__class__.__name__)
    # params_list = list_from_xlsx('files/tab p2.xlsx')
    # params_source = [get_str_K1237(row) for row in params_list]
    # print(params_source)
    # k2 = K1237.get(K1237.id==1).k2
    k1237 = K1237.get(K1237.id == 1)
    print(k1237.k2, k1237.k3)
    # aa = {'hcs_name': 'Этилмеркаптан', 'hcs_form': '(C2H5SH)', 'gas_density': None, 'liquid_density': 0.839, 'boiling_t': 35.0, 'toxodeth': 2.2, 'k1': 0.0, 'k2': 0.028, 'k3': 0.27, 'k7_1': '[0.1, 0.2, 0.5, 1.0, 1.7]', 'k7_1_f': '-1.85288457211878e-22*x**4 - 1.6940658945086e-21*x**3 + 0.00025*x**2 + 0.02*x + 0.5', 'k7_2': None, 'k7_2_f': None}

    # with db.atomic():
    #     K1237.insert_many(params_source).execute()
