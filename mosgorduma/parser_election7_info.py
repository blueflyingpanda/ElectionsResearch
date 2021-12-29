"""
Программа парсит сведения о кандидатах выборов депутатов Московской городской Думы седьмого созыва по
одномандатному (многомандатному) округу. Результаты сохраняются в файл info7.csv c полями
single_mandate -> номер округа
declined -> кол-во отказов
"""

import ssl
import time
from urllib import request
import os


def parse_page(link, single_mandate):
    req = request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    file = request.urlopen(req)
    html = file.read().decode('windows-1251')  # windows-1251
    declined = [i for i in range(len(html)) if html.startswith('отказ в регистрации', i) or
                html.startswith('выбывший (после регистрации) кандидат', i)]
    return str(single_mandate) + ',' + str(len(declined)) + '\n'


def main():
    ssl._create_default_https_context = ssl._create_unverified_context
    link_left = 'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd='
    link_right = '&vrn=27720002327736&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=27720002327736&report_mode=null'
    link_mids = (
        '27720002327741',
        '27720002327747',
        '27720002327752',
        '27720002327756',
        '27720002327760',
        '27720002327764',
        '27720002327769',
        '27720002327774',
        '27720002327779',
        '27720002327785',
        '27720002327789',
        '27720002327793',
        '27720002327797',
        '27720002327801',
        '27720002327807',
        '27720002327811',
        '27720002327815',
        '27720002327819',
        '27720002327824',
        '27720002327828',
        '27720002327834',
        '27720002327837',
        '27720002327841',
        '27720002327845',
        '27720002327850',
        '27720002327853',
        '27720002327857',
        '27720002327860',
        '27720002327864',
        '27720002327868',
        '27720002327871',
        '27720002327875',
        '27720002327880',
        '27720002327883',
        '27720002327887',
        '27720002327890',
        '27720002327894',
        '27720002327899',
        '27720002327905',
        '27720002327911',
        '27720002327915',
        '27720002327919',
        '27720002327923',
        '27720002327927',
        '27720002327932'
    )
    single_mandate = 1
    csv = 'single_mandate,declined\n'
    file = open('info7.csv', 'w')
    for link_mid in link_mids:
        print(single_mandate)
        percent = int(single_mandate * 100 / 45)
        space = 100 - percent
        print('LOADING:', '[' + '|' * percent + ' ' * space + ']', str(percent) + '%')
        # os.system('clear')
        file.write(csv)
        csv = parse_page(link_left + link_mid + link_right, single_mandate)
        # time.sleep(9)
        single_mandate += 1
    file.write(csv)
    file.close()


if __name__ == '__main__':
    main()
