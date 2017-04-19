from astral import Astral
from datetime import datetime, date, time, timedelta, tzinfo
import time as t

# figure out the degree of vertical stability of air

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
dtime = time(0, 0)
dt = date(2017, 4, 19)
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


def time_of_day(dt, city_name):
    a = Astral()
    # a.solar_depression = 'civil'
    city = a[city_name]
    sun = city.sun(date=dt.date(), local=True)
    sunrise = sun['sunrise'].replace(tzinfo=None)
    sunrise_tomorrow = city.sun(date=dt.date() + timedelta(days=1), local=True)['sunrise'].replace(tzinfo=None)
    sunset_yesterday = city.sun(date=dt.date() - timedelta(days=1), local=True)['sunset'].replace(tzinfo=None)
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
        elif (sunset + timedelta(hours=2)).replace(tzinfo=None) < dt < sunrise_tomorrow:
            return 'night'
    elif dt > sunset_yesterday + timedelta(hours=2):
        return 'night'

print('timedelta: %s' % (sun['sunrise'] + timedelta(hours=2)).replace(tzinfo=None))
print(dt)
print(dt - sun['sunrise'].replace(tzinfo=None))
print('time of day: %s' % time_of_day(dt, 'Moscow'))

# Под термином «утро» понимается период времени в течение 2 ч после восхода солнца
# под термином «вечер» - в течение 2 ч после захода солнца
# Период от восхода до захода солнца за вычетом двух утренних часов - день, а период от захода до восхода солнца за вычетом двух вечерних часов - ночь.

# if (sun['sunrise'] < T < sun['sunset']) and (light < threshold):
