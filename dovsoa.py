from astral import Astral
from datetime import datetime, date, time, timedelta, tzinfo

import sympy

## evaluate the degree of vertical stability of air
city_name = 'Moscow'


### a.solar_depression = 'civil'
# a = Astral()
# city = a[city_name]
# sun = city.sun(date=datetime.today().date(), local=True)

# print('Восход: %s' % sun['sunrise'].time())
#
# print(datetime.time(datetime.now()))

# dtime = time(7, 30)
# dt = date(2017, 4, 19)
# dstamp = datetime.combine(dt, dtime).timestamp()
# dt = datetime.fromtimestamp(dstamp)
# dt = datetime.combine(dt, dtime)

#
# print('sunrise %s' % sun['sunrise'])
# print('sunset %s' % sun['sunset'])
# print('sunrise  delta %s' % (dt - sun['sunrise'].replace(tzinfo=None)))
#
#
# print('dt : %s' % dt)
# print('date: %s; timestamp: %s' % (dt.date(), dstamp))
# print('time: %s' % dt.time())
#
#
# print('tzinfo %s ' % datetime.utcnow())

import math


# evaluate the degree of vertical stability of air

city_name = 'Moscow'
a = Astral()

# a.solar_depression = 'civil'
city = a[city_name]
sun = city.sun(date=datetime.today().date(), local=True)

print('Восход: %s' % sun['sunrise'].time())

print(datetime.time(datetime.now()))
# datetime.combine(date, time) - объект datetime из комбинации объектов date и time.
# print(datetime.datetime.time(13, 30))
# timestamp = datetime.today().timestamp()
# dtime = time(7, 0)
# dtime = time()
dtime = datetime.now().time()

# dt = date(2017, 4, 19)
dt = datetime.now()
dstamp = datetime.combine(dt, dtime).timestamp()

dt = datetime.fromtimestamp(dstamp)

print('sunrise %s' % sun['sunrise'])
print('sunset %s' % sun['sunset'])
print('sunrise  delta %s' % (dt - sun['sunrise'].replace(tzinfo=None)))
# print('Разность: %s' % datetime.combine(dt, dtime) - sun['sunrise'])

print('dt : %s' % dt)
print('date: %s; timestamp: %s' % (dt.date(), dstamp))
print('time: %s' % dt.time())
# time.mktime(dt.timetuple()) # Вот, а это timestamp
# print(time.mktime(dt.timetuple()))

print('tzinfo %s ' % datetime.utcnow())


# нахождение времени суток
def time_of_day(dt, city_name):
    a = Astral()
    # a.solar_depression = 'civil'
    city = a[city_name]
    sun = city.sun(date=dt.date(), local=True)
    sunrise = sun['sunrise'].replace(tzinfo=None)

    start_earth_day = datetime.combine(dt.date(), time(0, 0))
    end_earth_day = datetime.combine(dt.date(), time(23, 59))
    sunset = sun['sunset'].replace(tzinfo=None)

    if dt > sunrise:
        if (sunrise + timedelta(hours=2)).replace(tzinfo=None) < dt < sunset:
            return 'day'
        elif dt - sunrise <= timedelta(hours=2):
            print('dt : %s' % dt)
            print('sunrise %s' % sunrise)
            print('dt - sunrise %s' % (dt - sunrise))
            return 'morning'
        elif dt - sunset <= timedelta(hours=2):
            return 'evening'
        elif (sunset + timedelta(hours=2)).replace(tzinfo=None) < dt <= end_earth_day:
            return 'night'
    elif dt >= start_earth_day:
        return 'night'


# Определение степени вертикальной устойчивости воздуха по прогнозу погоды
def get_dovsoa(wind_speed, time_of_day, cloudiness=False, snow=False):
    # cloudiness - облачность
    # снег - наличие снежного покрова
    if type(snow) != bool and type(cloudiness) != bool:
        return None

    wind_speed_r = float(wind_speed)
    if wind_speed_r < 2:
        wind_speed = 'V<2'
    elif 2 <= wind_speed_r <= 3.9:
        wind_speed = '2<=V<=3.9'
    elif wind_speed_r > 4:
        wind_speed = 'V>4'

    if time_of_day not in ['morning', 'night', 'day', 'evening']:
        return None

    dovsoa_list = [
        {'wind_speed': 'V<2', 'snow': False, 'cloudiness': False,
         'night':'ин', 'morning': 'из', 'day': 'к', 'evening':'ин'},
        {'wind_speed': 'V<2', 'snow': True, 'cloudiness': True,
         'night': 'из', 'morning': 'из', 'day': 'из', 'evening': 'из'},
        {'wind_speed': 'V<2', 'snow': True, 'cloudiness': False,
         'night': 'ин', 'morning': 'ин', 'day': 'из', 'evening': 'ин'},
        {'wind_speed': 'V<2', 'snow': False, 'cloudiness': True,
         'night': 'из', 'morning': 'из', 'day': 'из', 'evening': 'из'},

        {'wind_speed': '2<=V<=3.9', 'snow': False, 'cloudiness': False,
         'night':'ин', 'morning': 'из', 'day': 'из', 'evening': 'из'},
        {'wind_speed': '2<=V<=3.9', 'snow': True, 'cloudiness': True,
         'night': 'из', 'morning': 'из', 'day': 'из', 'evening': 'из'},
        {'wind_speed': '2<=V<=3.9', 'snow': True, 'cloudiness': False,
         'night': 'ин', 'morning': 'ин', 'day': 'из', 'evening': 'ин'},
        {'wind_speed': '2<=V<=3.9', 'snow': False, 'cloudiness': True,
         'night': 'из', 'morning': 'из', 'day': 'из', 'evening': 'из'},

        {'wind_speed': 'V>4', 'snow': False, 'cloudiness':False,
         'night':'из', 'morning': 'из', 'day': 'из', 'evening':'из'},
        {'wind_speed': 'V>4', 'snow': True, 'cloudiness': True,
         'night': 'из', 'morning': 'из', 'day': 'из', 'evening': 'из'},
        {'wind_speed': 'V>4', 'snow': True, 'cloudiness': False,
         'night': 'из', 'morning': 'из', 'day': 'из', 'evening': 'из'},
        {'wind_speed': 'V>4', 'snow': False, 'cloudiness': True,
         'night': 'из', 'morning': 'из', 'day': 'из', 'evening': 'из'},
     ]
    return [x[time_of_day] for x in dovsoa_list if x['snow'] == snow and
            x['wind_speed'] == wind_speed and x['cloudiness'] == cloudiness][0]


# print('timedelta: %s' % (sun['sunrise'] + timedelta(hours=2)).replace(tzinfo=None))
# print(dt)
# print(dt - sun['sunrise'].replace(tzinfo=None))
# print('time of day: %s' % time_of_day(dt, 'Moscow'))
#
# print(get_dovsoa(1, 'day', cloudiness=False, snow=False))


# print(get_k7([0.1, 0.2, 0.1, 1, 2.2], 35))

#
if __name__ == '__main__':
    print('timedelta: %s' % (sun['sunrise'] + timedelta(hours=2)).replace(tzinfo=None))
    print(dt)
    print(dt - sun['sunrise'].replace(tzinfo=None))
    print('Время суток: %s' % time_of_day(dt, 'Moscow'))
    print(get_dovsoa(1, time_of_day(dt, 'Moscow'), cloudiness=False, snow=False))
    # print(get_k7([0.1, 0.2, 0.1, 1, 2.2], 35))


# Под термином «утро» понимается период времени в течение 2 ч после восхода солнца
# под термином «вечер» - в течение 2 ч после захода солнца
# Период от восхода до захода солнца за вычетом двух утренних часов - день, а период от захода до восхода солнца за вычетом двух вечерних часов - ночь.

# if (sun['sunrise'] < T < sun['sunset']) and (light < threshold):
