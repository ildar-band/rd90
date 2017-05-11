from k1237 import *
from params import *
from dovsoa import *

k1237 = K1237.get(K1237.id == 1)



# Определение эквивалентного количества вещества в первичном облаке


# def equivalent_amount_1(k1237, dovsoa, air_t, substance_mount):
#     # Определение эквивалентного количества вещества в первичном облаке Qэ1 = К1 К3 К5 К7 Q0
#     return get_k1(k1237) * k1237.k3 * get_k5(dovsoa) * get_k7(k1237, air_t, cloud=1) * \
#            get_substance_mount(substance_mount, k1237)

# def equivalent_amount_2(k1237, dovsoa, air_t, substance_mount, wind_speed, under_press = 'no_pressure'):
#     # Определение эквивалентного количества вещества во вторичном облаке Qэ2 = (1 - К1) К2 К3 К4 К5 К6 К7
#     return (1 - get_k1(k1237, under_press)) * k1237.k2 * k1237.k3 * get_k4(wind_speed) * get_k5(dovsoa) * \
#            get_k7(k1237, air_t, cloud=1) * substance_mount


if __name__ == '__main__':
    # 1. Определение степени вертикальной устойчивости воздуха по метеоинформации
    dtime = time(7, 30) # Время
    dt = date(2017, 4, 19) # Дата
    dt = datetime.combine(dt, dtime)

    city_name = 'Moscow'
    time_of_day = time_of_day(dt, city_name) # время дня

    dovsoa = get_dovsoa(11, time_of_day)
    print('1. Определение степени вертикальной устойчивости воздуха по метеоинформации: %s' % dovsoa)

    # 2. Определение эквивалентного количества вещества в первичном облаке

    air_t = 20  # температура воздуха
    q = 10 # количество выброшенного (разлившегося) при аварии вещества, т


    K1237 = Coeff(1, 10, dovsoa, air_t, dt, datetime(2017,4,19,8,30), 'liquid')

    # equivalent_amount_1(k1237, dovsoa, air_t, q)

    # k4 = get_k4(5)
    # print(k4)




    # 3. Определение эквивалентного количества вещества во вторичном облаке







