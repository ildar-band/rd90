from xlsxing import list_from_xlsx
import sympy
import re

def get_xslx_str_K1237_to_db(params_line_from_file):
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

if __name__ == '__main__':

    # db.create_tables([K1237], safe=True)
    print(K1237._meta.fields)
    print(K1237.__class__.__name__)
    # params_list = list_from_xlsx('files/tab p2.xlsx')
    # params_source = [get_str_K1237(row) for row in params_list]
    # print(params_source)
    # k2 = K1237.get(K1237.id==1).k2

    # aa = {'hcs_name': 'Этилмеркаптан', 'hcs_form': '(C2H5SH)', 'gas_density': None, 'liquid_density': 0.839, 'boiling_t': 35.0, 'toxodeth': 2.2, 'k1': 0.0, 'k2': 0.028, 'k3': 0.27, 'k7_1': '[0.1, 0.2, 0.5, 1.0, 1.7]', 'k7_1_f': '-1.85288457211878e-22*x**4 - 1.6940658945086e-21*x**3 + 0.00025*x**2 + 0.02*x + 0.5', 'k7_2': None, 'k7_2_f': None}

    # with db.atomic():
    #     K1237.insert_many(params_source).execute()