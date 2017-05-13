from k1237 import *
from params import *
from dovsoa import *
from datetime import datetime, date, timedelta

k1237 = K1237.get(K1237.id == 1)



# Определение эквивалентного количества вещества в первичном облаке


def equivalent_amount_1(coef, substance_mount):
    # Определение эквивалентного количества вещества в первичном облаке Qэ1 = К1 К3 К5 К7 Q0
    return coef.k1 * coef.k3 * coef.k5 * coef.k7 * substance_mount

    # * get_k7(k1237, air_t, cloud=1) * \
    #        get_substance_mount(substance_mount, k1237)

def equivalent_amount_2(coef,substance_mount):
    # Определение эквивалентного количества вещества во вторичном облаке Qэ2 = (1 - К1) К2 К3 К4 К5 К6 К7
    return (1 - coef.k1) * coef.k2 * coef.k3 * coef.k4 * coef.k5 * coef.k6 * coef.k7 * substance_mount / (coef.layer_thickness * coef.density)


if __name__ == '__main__':
    # 1. Определение степени вертикальной устойчивости воздуха по метеоинформации
    dtime = time(2, 30) # Время
    dt = date(2017, 4, 19) # Дата
    dt = datetime.combine(dt, dtime)

    city_name = 'Moscow'
    time_of_day = time_of_day(dt, city_name) # время дня

    dovsoa = get_dovsoa(11, time_of_day)
    air_t = 20  # температура воздуха
    q = 12 # количество выброшенного (разлившегося) при аварии вещества, т


    # cloud_1_coef = Coeff(1, 2, dovsoa, air_t, dt, datetime(2017,4,19,8,30), 'liquid', 1)
    # cloud_2_coef = Coeff(1, 2, dovsoa, air_t, dt, datetime(2017,4,19,8,30), 'liquid', 2)
    #
    cloud_1_coef = Coeff(30, 2, dovsoa, air_t, dt, datetime(2017,4,19,3,30), 'liquid', 1)
    cloud_2_coef = Coeff(30, 2, dovsoa, air_t, dt, datetime(2017,4,19,3,30), 'liquid', 2)
    print('1. Определение степени вертикальной устойчивости воздуха по метеоинформации: \n%s' % dovsoa)

    print("2. Определение эквивалентного количества вещества в первичном облаке: \n%s"
          % equivalent_amount_1(cloud_1_coef, q))

    print("2. Определение эквивалентного количества вещества во вторичном облаке: \n%s"
      % equivalent_amount_2(cloud_2_coef, q))


    # equivalent_amount_1(k1237, dovsoa, air_t, q)

    # k4 = get_k4(5)
    # print(k4)




    # 3. Определение эквивалентного количества вещества во вторичном облаке







