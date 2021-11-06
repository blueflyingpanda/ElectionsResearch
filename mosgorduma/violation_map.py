"""
Программа парсит данные Карты Нарушений на выборах 8 сентября 2019
если в сообщении о нарушении не указан уик - сообщение не учитывается
Результаты сохраняются в файл violation_map.csv c полями
_ -> id (pandas)
single_mandate -> номер округа
uik -> номер уика
violations -> кол-во нарушений
"""

import ssl
from urllib import request
from bs4 import BeautifulSoup
import pandas as pd


def main():
    ssl._create_default_https_context = ssl._create_unverified_context
    link = 'https://www.kartanarusheniy.org/2019-09-08/s/3928382754?page='
    uiks_to_violations = dict()
    df = pd.read_csv('mandates_to_districts_to_uiks.csv', dtype=str)
    for page in range(1, 16):
        print('page', page)
        req = request.Request(link + str(page), headers={'User-Agent': 'Mozilla/5.0'})
        file = request.urlopen(req)
        html = file.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        violations = soup.find_all('div', class_='kn__b kn__b--msg')
        for violation in violations:
            v = violation.find('div', class_='kn__msg-tags--group')
            if v.get_text() == 'УИК №':
                uik = v.find_next_sibling("div").get_text().strip('\n')
                uiks_to_violations[uik] = uiks_to_violations.get(uik, 0) + 1
    violations_array = []
    for u in df['uik']:
        violations_array.append(uiks_to_violations.get(u, 0))
    df['violations'] = violations_array
    df.to_csv('violation_map.csv', sep=',', encoding='utf-8')


if __name__ == '__main__':
    main()
