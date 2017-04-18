from astral import Astral
import datetime

# figure out the degree of vertical stability of air

city_name = 'Moscow'
a = Astral()

# a.solar_depression = 'civil'
city = a[city_name]
sun = city.sun(date=datetime.date(2017, 4, 18), local=True)

print(sun['sunrise'])
# morning
# evening
# day
# night

#



# Под термином «утро» понимается период времени в течение 2 ч после восхода солнца
# под термином «вечер» - в течение 2 ч после захода солнца
# Период от восхода до захода солнца за вычетом двух утренних часов - день, а период от захода до восхода солнца за вычетом двух вечерних часов - ночь.

# if (sun['sunrise'] < T < sun['sunset']) and (light < threshold):
