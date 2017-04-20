from peewee import *

# degree of vertical stability of air
# db_dovsoa = SqliteDatabase('files/dovsoa.db')


def get_dovsoa(wind_speed, time_of_day, cloudiness=False, snow=False):

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
            x['wind_speed'] == wind_speed and x['cloudiness'] == cloudiness]


print(get_dovsoa(1, 'day', cloudiness=False, snow=False))
