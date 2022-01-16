import ssl
from utils.progress_bar import show_progress_bar
from selenium import webdriver
import bs4

browser = webdriver.Chrome()


def collide_two_lists(lst1: list, lst2: list):
    res = []
    for i in range(min(len(lst1), len(lst2))):
        res.append(lst1[i])
        res.append(lst2[i])
    if len(lst1) != len(lst2):
        res.append(lst1[len(lst2)])
    return res


def parse_page_info(link):
    link_end = 1
    csv_part = ''
    while True:
        browser.get(link + str(link_end))
        html_source = browser.page_source
        soup = bs4.BeautifulSoup(html_source, 'html.parser')
        if soup.find('td', {"class": "dataTables_empty"}):
            break
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
        print(link_end)
        link_end += 1
    return csv_part

def parse_page_results(link):
    csv_part = ''
    browser.get(link)
    html_source = browser.page_source
    soup = bs4.BeautifulSoup(html_source, 'html.parser')
    rows = soup.find_all('h1', {"class": "report-title"})
    ds = rows[0].text
    district = ds[ds.find('округа') + len('округа') + 1:]
    rows = soup.find_all('td', {"class": "text-left"})
    rows = rows[12:]
    candidates = [r.text for r in rows]
    rows = soup.find_all('td', {"class": "text-center"})
    txt = rows[0].text
    mandate = txt.split('№')[1].strip()
    rows = soup.find_all('td', {"class": "text-right"})
    potential_voters = int(rows[1].text)
    inside_voters = int(rows[3].text)
    early_voters = int(rows[4].text)
    outside_voters = int(rows[5].text)
    attendance = (inside_voters + early_voters + outside_voters) * 100 / potential_voters
    early = early_voters * 100 / potential_voters
    outside = outside_voters * 100 / potential_voters
    rows = rows[13:]
    votes = [r.text for r in rows]
    for i in range(len(candidates)):
        csv_part += f'{candidates[i]},{district},{mandate},{votes[i]},{potential_voters},{inside_voters},{early_voters},{outside_voters},{attendance},{early},{outside}\n'
    return csv_part


def parse_election_info2017():
    link_left = 'http://www.moscow-city.vybory.izbirkom.ru/region/region/moscow-city?action=show&root=1&tvd='
    link_right = '&vrn=4774001137457&region=77&global=null&sub_region=77&prver=0&pronetvd=null&cuiknum=null&report_mode=null&type=220&number='
    link_mids = (
        '4774001137463',
        '4774001137464',
        '4774001137465',
        # '4774002138804',
        # '4774002138805',
        # '4774002138806',
        # '4774003123938',
        # '4774003123939',
        # '4774012107877',
        # '4774012107878',
    )
    csv = 'name,declined,parties,won\n'
    file = open('info2017.csv', 'w')
    district = 1
    for link_mid in link_mids:
        show_progress_bar(district, mandates=125)
        district += 1
        file.write(csv)
        csv = parse_page_info(link_left + link_mid + link_right)
        district += 1
        # time.sleep(9)
    file.write(csv)
    file.close()

def parse_election_results2017():
    ssl._create_default_https_context = ssl._create_unverified_context
    link_left = 'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd='
    link_right = '&vrn=4774004151542&prver=0&pronetvd=null&region=77&sub_region=77&type=426&report_mode=null'
    link_mids = (
        '4774001137463',
        '4774001137464',
        '4774001137465',
        '4774002138804',
        '4774002138805',
        '4774002138806',
        '4774003123938',
        '4774003123939',
        '4774012107877',
        '4774012107878',
    )
    csv = 'name,district,mandate,votes,potential_voters,inside_voters,early_voters,outside_voters,attendance,early,outside\n'
    file = open('data2017.csv', 'w')
    district = 1
    for link_mid in link_mids:
        show_progress_bar(district, mandates=125)
        file.write(csv)
        csv = parse_page_results(link_left + link_mid + link_right)
        district += 1
        # time.sleep(9)
    file.write(csv)
    file.close()

