from k1237 import *
from params import *
from dovsoa import *
from datetime import datetime, date, timedelta
import scipy.interpolate
import math

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

def contamination_depth(equivalent_amount, wind_speed):
    '''
    :param equivalent_amount:
    :param wind_speed:
    :return:
    '''
    x = [0.01, 0.05, 0.1, 0.5, 1, 3, 5, 10, 20, 30, 50, 70, 100, 300, 500, 700, 1000, 2000]
    y = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    z = [
        [0.38, 0.85, 1.25, 3.16, 4.75, 9.18, 12.53, 19.20, 29.56, 38.13, 52.67, 65.23, 81.91, 166, 231, 288, 363, 572],
        [0.26, 0.59, 0.84, 1.92, 2.84, 5.35, 7.20, 10.83, 16.44, 21.02, 28.73, 35.35, 44.09, 87.79, 121, 150, 189, 295],
        [0.22, 0.48, 0.68, 1.53, 2.17, 3.99, 5.34, 7.96, 11.94, 15.18, 20.59, 25.21, 31.30, 61.47, 84.50, 104, 130, 202],
        [0.19, 0.42, 0.59, 1.33, 1.88, 3.28, 4.36, 6.46, 9.62, 12.18, 16.43, 20.05, 24.80, 48.18, 65.92, 81.17, 101, 157],
        [0.17, 0.38, 0.53, 1.19, 1.68, 2.91, 3.75, 5.53, 8.19, 10.33, 13.88, 16.89, 20.82, 40.11, 54.67, 67.15, 83.60, 129],
        [0.15, 0.34, 0.48, 1.09, 1.53, 2.66, 3.43, 4.88, 7.20, 9.06, 12.14, 14.79, 18.13, 34.67, 47.09, 56.72, 71.70, 110],
        [0.14, 0.32, 0.45, 1.00, 1.42, 2.46, 3.17, 4.49, 6.48, 8.14, 10.87, 13.17, 16.17, 30.73, 41.63, 50.93, 63.16, 96.30],
        [0.13, 0.30, 0.42, 0.94, 1.33, 2.30, 2.97, 4.20, 5.92, 7.42, 9.90, 11.98, 14.68, 27.75, 37.49, 45.79, 56.70, 86.20],
        [0.12, 0.28, 0.40, 0.88, 1.25, 2.17, 2.80, 3.96, 5.60, 6.86, 9.12, 11.03, 13.50, 25.39, 34.24, 41.76, 51.60, 78.30],
        [0.12, 0.26, 0.38, 0.84, 1.19, 2.06, 2.66, 3.76, 5.31, 6.50, 8.50, 10.23, 12.54, 23.49, 31.61, 38.50, 47.53, 71.90],
        [0.11, 0.25, 0.36, 0.80, 1.13, 1.96, 2.53, 3.58, 5.06, 6.20, 8.01, 9.61, 11.74, 21.91, 29.44, 35.81, 44.15, 66.62],
        [0.11, 0.24, 0.34, 0.76, 1.08, 1.88, 2.42, 3.43, 4.85, 5.94, 7.67, 9.07, 11.06, 20.58, 27.61, 35.55, 41.30, 62.20],
        [0.10, 0.23, 0.33, 0.74, 1.04, 1.80, 2.37, 3.29, 4.66, 5.70, 7.37, 8.72, 10.48, 19.45, 26.04, 31.62, 38.90, 58.44],
        [0.10, 0.22, 0.32, 0.71, 1.00, 1.74, 2.24, 3.17, 4.49, 5.50, 7.10, 8.40, 10.04, 18.46, 24.69, 29.95, 36.81, 55.20],
        [0.10, 0.22, 0.31, 0.69, 0.97, 1.68, 2.17, 3.07, 4.34, 5.31, 6.86, 8.11, 9.70, 17.60, 23.50, 28.48, 34.98, 52.37]
    ]
    f = scipy.interpolate.interp2d(x, y, z, kind='linear')
    return f(equivalent_amount, wind_speed)[0]


print('Глубина зоны заражения: %s км.' % contamination_depth(620, 13))

def get_front_speed(wind_speed, dovsoa):
    '''
    :param wind_speed: скорость ветра м/с
    :param dovsoa: состояние атмосферы (степень вертикальной устойчивости)
    :return: скорость переноса переднего фронта облака зараженного воздуха в зависимости от скорости ветра
    '''
    wind_speed_i = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    invers_speed = [0, 5, 10, 16, 21]
    konvek_speed = [0, 7, 14, 21, 28]
    isoterm_speed = [6, 12, 18, 24, 29, 35, 41, 47, 53, 59, 65, 71, 76, 82, 88]
    value_list = list(zip(wind_speed_i, isoterm_speed))
    if dovsoa == 'из':
        f = scipy.interpolate.interp1d(wind_speed_i, isoterm_speed, bounds_error=False, fill_value="extrapolate")
        return f(wind_speed)
    if dovsoa == 'ин' and wind_speed in range(1, 4):
        return invers_speed[wind_speed]
    if dovsoa == 'к' and wind_speed in range(1, 4):
        return konvek_speed[wind_speed]


def get_contamination_depth(contamination_depth_1, contamination_depth_2, front_speed, after_crash_time):
    '''
    :param contamination_depth_1:
    :param contamination_depth_2:
    :param front_speed:
    :param after_crash_time:
    :return:
    '''
    max_contamination_depth = max(contamination_depth_1, contamination_depth_2) + \
                              0.5 * min(contamination_depth_1, contamination_depth_2)
    possible_depth = front_speed * after_crash_time
    return min(max_contamination_depth, possible_depth)


def get_possible_contamination_area(contamination_depth, wind_speed):
    '''
    :param contamination_depth:
    :param wind_speed:
    :return: площадь зоны возможного заражения АХОВ
    '''
    if wind_speed <= 0.5:
        fi = 360
    if 0.6 <= wind_speed <= 1:
        fi = 180
    if 1.1 <= wind_speed <= 2:
        fi = 90
    if wind_speed > 2:
        fi = 45
    contamination_area = (math.pi * contamination_depth ** 2 * fi) / 360
    return contamination_area

def get_actual_contamination_area(contamination_depth, dovsoa, after_crash_time):
    '''
    :param contamination_depth:
    :param dovsoa:
    :param after_crash_time:
    :return: площадь зоны возможного заражения АХОВ
    '''
    k8_list = {'ин': 0.081, 'из': 0.133, 'к': 0.235}
    actual_contamination_area = k8_list[dovsoa] * contamination_depth ** 2 * after_crash_time ** 0.2
    return actual_contamination_area

print('скорость переноса переднего фронта %s' % get_front_speed(16,  'из'))


if __name__ == '__main__':
    # 1. Определение степени вертикальной устойчивости воздуха по метеоинформации
    crash_time = time(2, 30)  # Время
    crash_date = date(2017, 4, 19)  # Дата
    crash_dtime = datetime.combine(crash_date, crash_time)

    city_name = 'Moscow'
    time_of_day = time_of_day(crash_dtime, city_name) # время дня

    estimated_dtime = datetime(2017, 4, 19, 3, 30)
    after_crash_time = estimated_dtime - crash_dtime

    dovsoa = get_dovsoa(11, time_of_day)
    air_t = 20  # температура воздуха
    q = 12  # количество выброшенного (разлившегося) при аварии вещества, т
    wind_speed = 2  # скорость ветра
    hcs_id = 30  # id вещества
    hcs_storage = 'liquid'  # условия хранения АХОВ

    json_args = {
        
    }




    # cloud_1_coef = Coeff(1, 2, dovsoa, air_t, dt, datetime(2017,4,19,8,30), 'liquid', 1)
    # cloud_2_coef = Coeff(1, 2, dovsoa, air_t, dt, datetime(2017,4,19,8,30), 'liquid', 2)
    #
    cloud_1_coef = Coeff(hcs_id, wind_speed, dovsoa, air_t, after_crash_time, hcs_storage, 1)
    cloud_2_coef = Coeff(hcs_id, wind_speed, dovsoa, air_t, after_crash_time, hcs_storage, 2)
    print('1. Определение степени вертикальной устойчивости воздуха по метеоинформации: \n%s' % dovsoa)

    eq_amount_1 = equivalent_amount_1(cloud_1_coef, q)
    print("2. Определение эквивалентного количества вещества в первичном облаке: \n%s"
          % eq_amount_1)

    eq_amount_2 = equivalent_amount_2(cloud_2_coef, q)
    print("3. Определение эквивалентного количества вещества во вторичном облаке: \n%s"
      % equivalent_amount_2(cloud_2_coef, q))

    print("4. Продолжительность поражающего действия АХОВ: \n%s"
      % cloud_2_coef.evaporation_duration)

    contamination_depth_1 = contamination_depth(eq_amount_1, wind_speed)
    contamination_depth_2 = contamination_depth(eq_amount_2, wind_speed)
    front_speed = get_front_speed(wind_speed, dovsoa)
    depth = get_contamination_depth(contamination_depth_1, contamination_depth_2, front_speed, after_crash_time.total_seconds()/3600)
    print("5.Расчет глубины зоны заражения: \n%s"
      % depth)

    possible_contamination = get_possible_contamination_area(depth, wind_speed)
    print("4. Площадь зоены возможного заражения АХОВ: \n%s"
      % possible_contamination)

    actual_contamination = get_actual_contamination_area(depth, dovsoa, after_crash_time.total_seconds()/3600)
    print("4. Площадь зоены фактического заражения АХОВ: \n%s"
      % actual_contamination)
    # equivalent_amount_1(k1237, dovsoa, air_t, q)

    # k4 = get_k4(5)
    # print(k4)




    # 3. Определение эквивалентного количества вещества во вторичном облаке







