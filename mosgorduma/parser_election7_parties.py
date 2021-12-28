"""
Программа парсит сведения о кандидатах выборов депутатов Московской городской Думы седьмого созыва по
одномандатному (многомандатному) округу. Результаты сохраняются в файл info7.csv c полями
single_mandate -> номер округа
declined -> кол-во отказов
"""

import ssl
import time
from urllib import request


def parse_page(link):
    req = request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    file = request.urlopen(req)
    html = file.read().decode('windows-1251')  # windows-1251
    lb = html.find('<td>1</td><td class="text-left">')
    rb = html.find('</tbody>', lb)
    html = html[lb:rb]
    html = html.split('</tr>')
    csv = ''
    for line in html:
        if line.find('зарегистрирован') != -1:
            name = line[line.find('>', line.find('href=')) + 1:line.find('</a></td><td')]
            left_border = line.find('"text-left">', line.find('align="center"')) + 12
            right_border = line.find('</td><td align', line.find('align="center"'))
            party = line[left_border:right_border]
            csv += name + ',' + party + '\n'
    return csv.replace('"', '')


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
    csv = 'name,party\n'
    file = open('parties7.csv', 'w')
    for link_mid in link_mids:
        file.write(csv)
        csv = parse_page(link_left + link_mid + link_right)
        # time.sleep(9)
    file.write(csv)
    file.close()


if __name__ == '__main__':
    main()
