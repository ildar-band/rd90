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

for item in bs.find_all('th', 'pogodacell2'):
    print(item.text)
    print(item.next_sibling.next_sibling.text)