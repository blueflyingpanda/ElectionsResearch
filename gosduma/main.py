import sys
import time
from urllib import request
import ssl
import bs4
from selenium import webdriver
from pathlib import Path
from utils.progress_bar import show_progress_bar

browser = webdriver.Chrome()

ssl._create_default_https_context = ssl._create_unverified_context


def discover_winner2016(votes: list) -> list:
    index_max = 0
    max_votes = votes[0]
    wons = [False] * len(votes)
    for i in range(len(votes)):
        if int(max_votes) < int(votes[i]):
            max_votes = votes[i]
            index_max = i
    wons[index_max] = True
    return wons


def parse_page_results2016(link):
    csv_part = ''
    req = request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    file = request.urlopen(req)
    html = file.read().decode('windows-1251')  # windows-1251
    soup = bs4.BeautifulSoup(html, 'html.parser')
    rows = soup.find_all('td', {"class": "text-left"})
    rows = rows[18:]
    candidates = [r.text for r in rows]
    rows = soup.find_all('td', {"class": "text-center"})
    mandate = rows[0].text.split('–')[1].strip()
    potential_voters = int(rows[1].text)
    inside_voters = int(rows[4].text)
    early_voters = int(rows[3].text)
    outside_voters = int(rows[5].text)
    absentee = int(rows[13].text) / potential_voters * 100
    attendance = (inside_voters + early_voters + outside_voters) * 100 / potential_voters
    early = early_voters * 100 / potential_voters
    outside = outside_voters * 100 / potential_voters
    rows = rows[19:]
    votes = [r.text for r in rows]
    wons = discover_winner2016(votes)
    for i in range(len(candidates)):
        csv_part += f'{candidates[i]},{mandate},{votes[i]},{potential_voters},{inside_voters},{early_voters},{outside_voters},{attendance},{early},{outside},{absentee},{int(wons[i])}\n'
    return csv_part


def collide_two_lists(lst1: list, lst2: list):
    res = []
    for i in range(min(len(lst1), len(lst2))):
        res.append(lst1[i])
        res.append(lst2[i])
    if len(lst1) != len(lst2):
        res.append(lst1[len(lst2)])
    return res


def parse_page_info2016(link):
    csv_part = ''
    browser.get(link)
    html_source = browser.page_source
    soup = bs4.BeautifulSoup(html_source, 'html.parser')
    rows = soup.find_all('a', {"class": "list-link"})
    candidates = [r.text for r in rows]
    rows = soup.find_all('td')
    tmp = [r.text for r in rows]
    declined = tmp.count('отказ в регистрации')
    rows = soup.find_all('tr', {"class": "text-center even"})
    did_won_even = []
    parties_even = []
    registered_even = []
    for r in rows:
        tds = list(r.children)
        did_won_even.append(1 if tds[-2].text != ' ' else 0)
        parties_even.append(tds[4].text)
        registered_even.append(tds[7].text == 'зарегистрирован')
    rows = soup.find_all('tr', {"class": "text-center odd"})
    did_won_odd = []
    parties_odd = []
    registered_odd = []
    for r in rows:
        tds = list(r.children)
        did_won_odd.append(1 if tds[-2].text != ' ' else 0)
        parties_odd.append(tds[4].text)
        registered_odd.append(tds[7].text == 'зарегистрирован')
    did_won = collide_two_lists(did_won_odd, did_won_even)
    parties = collide_two_lists(parties_odd, parties_even)
    registered = collide_two_lists(registered_odd, registered_even)
    for i in range(len(candidates)):
        if registered[i]:
            csv_part += f'{candidates[i]},{declined},{parties[i]},{did_won[i]}\n'
    # print(link_end)
    return csv_part


def parse_election_results2016():
    link_left = 'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1000259&tvd='
    link_right = '&vrn=100100067795849&prver=0&pronetvd=null&region=77&sub_region=77&type=464&report_mode=null'
    link_mids = (
        '100100067796114',
        '100100067796115',
        '100100067796116',
        '100100067796117',
        '100100067796118',
        '100100067796119',
        '100100067796120',
        '100100067796121',
        '100100067796122',
        '100100067796123',
        '100100067796124',
        '100100067796125',
        '100100067796126',
        '100100067796127',
        '100100067796128'
    )
    mandates = len(link_mids)
    single_mandate = 1
    csv = 'name,single_mandate,votes,potential_voters,inside_voters,early_voters,outside_voters,attendance,early,outside,absentee,won\n'
    file = open('data2016.csv', 'w')
    for link_mid in link_mids:
        show_progress_bar(single_mandate, mandates=mandates)
        file.write(csv)
        csv = parse_page_results2016(link_left + link_mid + link_right)
        # time.sleep(9)
        single_mandate += 1
    file.write(csv)
    file.close()


def parse_election_info2016():
    link_left = 'http://www.vybory.izbirkom.ru/region/izbirkom?action=show&root=1000259&tvd='
    link_right = '&vrn=100100067795849&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=100100067795849&report_mode=null'
    link_mids = (
        '100100067796114',
        '100100067796115',
        '100100067796116',
        '100100067796117',
        '100100067796118',
        '100100067796119',
        '100100067796120',
        '100100067796121',
        '100100067796122',
        '100100067796123',
        '100100067796124',
        '100100067796125',
        '100100067796126',
        '100100067796127',
        '100100067796128',
    )
    mandates = len(link_mids)
    single_mandate = 1
    csv = 'name,declined,parties,won\n'
    file = open('info2016.csv', 'w')
    for link_mid in link_mids:
        show_progress_bar(single_mandate, mandates=mandates)
        file.write(csv)
        csv = parse_page_info2016(link_left + link_mid + link_right)
        # time.sleep(9)
        single_mandate += 1
    file.write(csv)
    file.close()

def convert_parties_to_numbers2016():
    file = open('info2016.csv', 'r')
    text = file.read()
    file2 = open('info2016.csv', 'w')
    text = text.replace('Самовыдвижение', '0')
    text = text.replace('Политическая партия КОММУНИСТИЧЕСКАЯ ПАРТИЯ КОММУНИСТЫ РОССИИ', '3')
    text = text.replace('Всероссийская политическая партия "ПАРТИЯ РОСТА"', '6')
    text = text.replace('Политическая партия "Гражданская Платформа"', '11')
    text = text.replace('Политическая партия "Российская объединенная демократическая партия "ЯБЛОКО"', '9')
    text = text.replace('Политическая партия ЛДПР – Либерально-демократическая партия России', '5')
    text = text.replace('Политическая партия СПРАВЕДЛИВАЯ РОССИЯ', '8')
    text = text.replace('Политическая партия "КОММУНИСТИЧЕСКАЯ ПАРТИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ"', '4')
    text = text.replace('Общественная организация Всероссийская политическая партия "Гражданская Сила"', '1')
    text = text.replace('Всероссийская политическая партия "ЕДИНАЯ РОССИЯ"', '10')
    text = text.replace('Политическая партия "Российская экологическая партия "Зеленые"', '2')
    text = text.replace('ВСЕРОССИЙСКАЯ ПОЛИТИЧЕСКАЯ ПАРТИЯ "РОДИНА"', '7')
    text = text.replace('Региональное отделение в городе Москве Всероссийской политической партии Социал-демократическая партия России', '12')
    text = text.replace('Политическая партия "Партия народной свободы" (ПАРНАС)', '13')
    text = text.replace('Политическая партия "ПАТРИОТЫ РОССИИ"', '14')
    file2.write(text)
    file.close()
    file2.close()


def form_clean_data2016():
    pass


def form_full_data2016():
    pass


def parse_election_results2021():
    pass


def parse_election_info2021():
    pass


def parse_election_parties2021():
    pass


def shortify_parties2021():
    pass


def form_clean_data2021():
    pass


def form_full_data2021():
    pass


def main():
    if len(sys.argv) != 2:
        print('election not specified!')
        exit(1)
    if sys.argv[1] == '2016':
        start_time = time.time()
        data = Path('data2016.csv')
        info = Path('info2016.csv')
        parties = Path('parties2016.csv')
        if not data.is_file() or not info.is_file() or not parties.is_file():
            # parse_election_results2016()
            print("DATA --- %s seconds ---" % (time.time() - start_time))
            # parse_election_info2016()
            print("INFO --- %s seconds ---" % (time.time() - start_time))
            convert_parties_to_numbers2016()
        print("PARTIES --- %s seconds ---" % (time.time() - start_time))
        # form_clean_data2016()  # hand data
        # form_full_data2016()  #  affiliation algo
        print("TOTAL --- %s seconds ---" % (time.time() - start_time))
    elif sys.argv[1] == '2021':
        pass
        # start_time = time.time()
        # data = Path('data2021.csv')
        # info = Path('info2021.csv')
        # parties = Path('parties2021.csv')
        # if not data.is_file() or not info.is_file() or not parties.is_file():
        #     parse_election_results2021()
        #     print("DATA --- %s seconds ---" % (time.time() - start_time))
        #     parse_election_info2021()
        #     print("INFO --- %s seconds ---" % (time.time() - start_time))
        #     parse_election_parties2021()
        # shortify_parties2021()
        # print("PARTIES --- %s seconds ---" % (time.time() - start_time))
        # form_clean_data2021()
        # form_full_data2021()
        # print("TOTAL --- %s seconds ---" % (time.time() - start_time))
    else:
        print('wrong year!')
        exit(1)


if __name__ == '__main__':
    sys.argv.append('2016')
    main()
    browser.close()