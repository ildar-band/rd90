import requests
from bs4 import BeautifulSoup

url = 'http://meteoinfo.ru/pogoda/russia/moscow-area/moscow'


def get_meteo_info_parse(url = 'http://meteoinfo.ru/pogoda/russia/moscow-area/moscow'):
    """
    :param url:
    :return: {'pressure': '720', 'humidity': '93', 'wind_direction': 'C-З', 'wind_speed': '2', 'clouding': '10', 'visibility': '4'}
    """
    html = get_html_meteo(url)
    if (html):
        bs = BeautifulSoup(html, 'html.parser')
        meteo_info = {}
        for item in bs.find_all('th', 'pogodacell2'):
            value = item.next_sibling.next_sibling.text
            # print(" %s : %s" % (item.text.lower(), value))
            if item.text.lower().find('давлени') > 0:
                meteo_info['pressure'] = value
            if item.text.lower().find('влажност') > 0:
                meteo_info['humidity'] = value
            if item.text.find('аправлени', 0) > 0:
                meteo_info['wind_direction'] = value
            if item.text.lower().find('корост') > 0:
                meteo_info['wind_speed'] = value
            if item.text.lower().find('облачност') > 0:
                meteo_info['clouding'] = value
            if item.text.lower().find('видимост') > 0:
                meteo_info['visibility'] = value
        return meteo_info
    else:
        return False


def get_html_meteo(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except requests.exceptions.RequestException:
        # print('Не получилось')
        return False

# определение степени вертикальной устойчивости воздуха
#
#TODO написать функцию   определяющую   ясно, переменная облачность или сплошная облачность
#Облачность выдается в баллах по 10-балльной шкале,
# 0 баллов = ясно,
# 1-3 балла = малооблачно,
# 4-7 баллов - облачно,
# 7-10 баллов - пасмурно.
# НГО - нижняя граница облаков - выдается в метрах.


# night, clear|partly cloudy, overcast

print(get_meteo_info_parse(url))