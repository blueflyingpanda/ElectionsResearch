"""
Программа парсит сведения о кандидатах выборов депутатов Московской городской Думы седьмого созыва по
одномандатному (многомандатному) округу. Результаты сохраняются в файл info6.csv c полями
single_mandate -> номер округа
declined -> кол-во отказов
"""

import ssl
from urllib import request
import time

def parse_page(link, single_mandate):
    req = request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    file = request.urlopen(req)
    html = file.read().decode('windows-1251')  # windows-1251
    declined = [i for i in range(len(html)) if html.startswith('отказ в регистрации', i) or
                html.startswith('выбывший (после регистрации) кандидат', i)]
    return str(single_mandate) + ',' + str(len(declined)) + '\n'


def main():
    ssl._create_default_https_context = ssl._create_unverified_context
    link_left = 'http://www.moscow-city.vybory.izbirkom.ru/region/region/moscow-city?action=show&root=1&tvd='
    link_right = '&vrn=27720001539308&region=77&global=&sub_region=77&prver=0&pronetvd=null&vibid=27720001539308&type=220'
    link_mids = (
        '27720001539819',
        '27720001539954',
        '27720001540044',
        '27720001540139',
        '27720001540226',
        '27720001540326',
        '27720001540404',
        '27720001540482',
        '27720001540571',
        '27720001540660',
        '27720001540741',
        '27720001540821',
        '27720001540891',
        '27720001540967',
        '27720001541063',
        '27720001541141',
        '27720001541223',
        '27720001541297',
        '27720001541385',
        '27720001541465',
        '27720001541543',
        '27720001541620',
        '27720001541696',
        '27720001541770',
        '27720001541873',
        '27720001541942',
        '27720001542009',
        '27720001542076',
        '27720001542157',
        '27720001542229',
        '27720001542304',
        '27720001542377',
        '27720001542472',
        '27720001542552',
        '27720001542648',
        '27720001542740',
        '27720001542821',
        '27720001542919',
        '27720001543021',
        '27720001543113',
        '27720001543196',
        '27720001543275',
        '27720001543361',
        '27720001543439',
        '27720001543525',
    )
    single_mandate = 1
    csv = 'single_mandate,declined\n'
    file = open('info6.csv', 'w')
    for link_mid in link_mids:
        file.write(csv)
        csv = parse_page(link_left + link_mid + link_right, single_mandate)
        # time.sleep(9)
        single_mandate += 1
    file.write(csv)
    file.close()


if __name__ == '__main__':
    main()
