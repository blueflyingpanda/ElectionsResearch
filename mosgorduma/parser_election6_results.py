"""
Программа парсит Сводные таблицы результатов выборов депутатов Московской городской Думы шестого созыва по
одномандатному (многомандатному) округу. Результаты сохраняются в файл data6.csv c полями
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
import time
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
    total_votes = int(inside_voters) + int(early_voters) + int(outside_voters)
    attendance = str(total_votes * 100 / int(potential_voters))
    early = str(int(early_voters) * 100 / total_votes)
    outside = str(int(outside_voters) * 100 / total_votes)
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
    link_left = 'http://www.moscow-city.vybory.izbirkom.ru/region/region/moscow-city?action=show&root=1&tvd='
    link_right = '&vrn=27720001539308&region=77&global=null&sub_region=77&prver=0&pronetvd=null&cuiknum=null&type=424'
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
        '27720001543525'
    )
    single_mandate = 1
    csv = 'name,single_mandate,votes,potential_voters,inside_voters,early_voters,outside_voters,attendance,early,outside,won\n'
    file = open('data6.csv', 'w')
    for link_mid in link_mids:
        file.write(csv)
        csv = parse_page(link_left + link_mid + link_right, single_mandate)
        # time.sleep(9)
        single_mandate += 1
    file.write(csv)
    file.close()


if __name__ == '__main__':
    main()
