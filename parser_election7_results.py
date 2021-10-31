"""
Программа парсит Сводные таблицы результатов выборов депутатов Московской городской Думы седьмого созыва по
одномандатному (многомандатному) округу. Результаты сохраняются в файл data.csv c полями
name -> ФИО кандидата
single_mandate -> номер округа
votes -> кол-во голосов, которые набрал кандидат
potential_voters -> кол-во потенциальных голосующих, числящихся за округом
inside_voters -> кол-во голосовавших на участке
early_voters -> кол-во проголосовавших заранее
outside_voters -> кол-во проголосовавших не на участке
attendance -> явка в процентах
early -> процент проголосовавших заранее от общего числа проголосовавших
outside -> процент проголосовавших не на участке от общего числа проголосовавших
won -> статус кандидата True - победил, False - проиграл
"""

import ssl
from urllib import request


def discover_winner(votes: list) -> list:
    index_max = 0
    max_votes = votes[0]
    wons = [False] * len(votes)
    for i in range(len(votes)):
        if int(max_votes) < int(votes[i]):
            max_votes = votes[i]
            index_max = i
    wons[index_max] = True
    return wons


def retrieve_general_info(html: str) -> tuple:
    html = html.split('<td class="fix-col first-fix-col"><nobr>7</nobr></td>')[0]
    html = html.split('</tr>')
    potential_voters = html[0][html[0].find('<nobr><b>') + 9:html[0].find('</b></nobr>')]
    inside_voters = html[2][html[2].find('<nobr><b>') + 9:html[2].find('</b></nobr>')]
    early_voters = html[3][html[3].find('<nobr><b>') + 9:html[3].find('</b></nobr>')]
    outside_voters = html[6][html[6].find('<nobr><b>') + 9:html[6].find('</b></nobr>')]
    attendance = str(
        round((int(inside_voters) + int(early_voters) + int(outside_voters)) / int(potential_voters) * 100, 2))
    early = str(round(int(early_voters) / int(potential_voters) * 100, 2))
    outside = str(round(int(outside_voters) / int(potential_voters) * 100, 2))
    return potential_voters, inside_voters, early_voters, outside_voters, attendance, early, outside


def retrieve_candidates_info(html: str) -> tuple:
    html = html.split('</tr>')
    candidates = []
    votes = []
    for part in html:
        if len(candidates) == len(html) - 1:
            break
        candidates.append(part[part.find('text-left">') + 11:part.find('</td><td class="fix-col third-fix-col')])
        votes.append(part[part.find('<nobr><b>') + 9:part.find('</b></nobr>')])
    return candidates, votes, discover_winner(votes)


def parse_page(link, single_mandate):
    csv_part = ''
    req = request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    file = request.urlopen(req)
    html = file.read().decode('windows-1251')  # windows-1251
    html = html[html.find('<table cell'):]
    html = html[:html.find('</table>')]
    html = html[html.find('<tbody>'):]
    html = html.split('<td class="fix-col first-fix-col"><nobr>10</nobr>')
    potential_voters, inside_voters, early_voters, outside_voters, attendance, early, outside = retrieve_general_info(
        html[0])
    candidates, votes, wons = retrieve_candidates_info(html[1])
    const = f"{potential_voters},{inside_voters},{early_voters},{outside_voters},{attendance},{early},{outside}"
    for i in range(len(candidates)):
        csv_part += f"{candidates[i]},{single_mandate},{votes[i]},{const},{wons[i]}\n"
    file.close()
    return csv_part


def main():
    ssl._create_default_https_context = ssl._create_unverified_context
    link_left = 'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd='
    link_right = '&vrn=27720002327736&prver=0&pronetvd=null&region=77&sub_region=77&type=424&report_mode=null'
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
    csv = 'name,single_mandate,votes,potential_voters,inside_voters,early_voters,outside_voters,attendance,early,outside,won\n'
    file = open('data.csv', 'w')
    for link_mid in link_mids:
        file.write(csv)
        csv = parse_page(link_left + link_mid + link_right, single_mandate)
        single_mandate += 1
    file.write(csv)
    file.close()


if __name__ == '__main__':
    main()
