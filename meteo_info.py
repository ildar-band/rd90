import requests
from bs4 import BeautifulSoup

url = 'http://meteoinfo.ru/pogoda/russia/moscow-area/moscow'



def get_html_meteo(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except requests.exceptions.RequestException:
        print('Не получилось')
        return False

html = get_html_meteo(url)

bs = BeautifulSoup(html, 'html.parser')
print(bs.title.text)
# print(bs.h1.text)
print('dsfasdfasd'.find('давление'))
meteo_info = {}

for item in bs.find_all('th', 'pogodacell2'):
    # print(item.text.lower())

    value = item.next_sibling.next_sibling.text
    print(" %s : %s" % (item.text.lower(), value))
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

    # print(item.next_sibling.next_sibling.text)

# определение степени вертикальной устойчивости воздуха
#
#TODO написать функцию   определяющую   ясно, переменная облачность или сплошная облачность



# night, clear|partly cloudy, overcast

print(meteo_info)