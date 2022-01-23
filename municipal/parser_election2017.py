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
    links = (
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774001137463&vrn=4774001137457&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774001137457&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774001137464&vrn=4774001137457&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774001137457&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774001137465&vrn=4774001137457&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774001137457&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774002138804&vrn=4774002138799&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774002138799&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774002138805&vrn=4774002138799&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774002138799&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774002138806&vrn=4774002138799&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774002138799&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774003123938&vrn=4774003123932&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774003123932&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774003123939&vrn=4774003123932&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774003123932&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774012107877&vrn=4774012107872&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774012107872&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774012107878&vrn=4774012107872&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774012107872&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774004151547&vrn=4774004151542&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774004151542&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774004151548&vrn=4774004151542&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774004151542&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774004151549&vrn=4774004151542&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774004151542&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774005159149&vrn=4774005159143&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774005159143&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774005159150&vrn=4774005159143&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774005159143&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774005159151&vrn=4774005159143&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774005159143&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774006133202&vrn=4774006133197&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774006133197&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774006133203&vrn=4774006133197&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774006133197&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774007117789&vrn=4774007117784&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774007117784&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774007117790&vrn=4774007117784&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774007117784&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774008112814&vrn=4774008112809&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774008112809&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774008112815&vrn=4774008112809&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774008112809&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774010120042&vrn=4774010120037&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774010120037&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774010120043&vrn=4774010120037&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774010120037&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774010120044&vrn=4774010120037&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774010120037&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774009134024&vrn=4774009134019&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774009134019&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774009134025&vrn=4774009134019&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774009134019&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774009134026&vrn=4774009134019&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774009134019&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774011164122&vrn=4774011164116&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774011164116&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774011164123&vrn=4774011164116&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774011164116&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774011164124&vrn=4774011164116&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774011164116&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774013126105&vrn=4774013126100&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774013126100&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774013126106&vrn=4774013126100&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774013126100&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774014127356&vrn=4774014127351&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774014127351&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774014127357&vrn=4774014127351&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774014127351&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774014127358&vrn=4774014127351&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774014127351&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774015125479&vrn=4774015125474&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774015125474&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774015125480&vrn=4774015125474&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774015125474&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774015125481&vrn=4774015125474&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774015125474&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774016123407&vrn=4774016123402&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774016123402&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774016123408&vrn=4774016123402&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774016123402&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774017109310&vrn=4774017109305&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774017109305&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774017109311&vrn=4774017109305&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774017109305&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774018119471&vrn=4774018119466&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774018119466&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774018119472&vrn=4774018119466&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774018119466&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774018119473&vrn=4774018119466&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774018119466&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774018119474&vrn=4774018119466&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774018119466&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774019123064&vrn=4774019123059&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774019123059&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774019123065&vrn=4774019123059&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774019123059&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774020142944&vrn=4774020142939&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774020142939&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774020142945&vrn=4774020142939&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774020142939&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774022146204&vrn=4774022146199&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774022146199&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774022146205&vrn=4774022146199&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774022146199&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774024151060&vrn=4774024151055&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774024151055&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774024151061&vrn=4774024151055&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774024151055&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774025130167&vrn=4774025130162&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774025130162&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774025130168&vrn=4774025130162&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774025130162&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774026116759&vrn=4774026116754&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774026116754&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774026116760&vrn=4774026116754&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774026116754&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774027138657&vrn=4774027138652&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774027138652&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774027138658&vrn=4774027138652&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774027138652&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774027138659&vrn=4774027138652&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774027138652&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774028131168&vrn=4774028131163&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774028131163&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774028131169&vrn=4774028131163&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774028131163&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774029131732&vrn=4774029131727&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774029131727&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774029131733&vrn=4774029131727&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774029131727&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774030117556&vrn=4774030117551&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774030117551&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774030117557&vrn=4774030117551&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774030117551&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774031150415&vrn=4774031150410&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774031150410&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774033139896&vrn=4774033139891&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774033139891&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774033139897&vrn=4774033139891&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774033139891&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774035127413&vrn=4774035127407&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774035127407&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774035127414&vrn=4774035127407&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774035127407&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774040125484&vrn=4774040125479&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774040125479&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774040125485&vrn=4774040125479&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774040125479&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774032129795&vrn=4774032129790&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774032129790&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774032129796&vrn=4774032129790&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774032129790&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774034121516&vrn=4774034121511&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774034121511&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774034121517&vrn=4774034121511&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774034121511&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774037132330&vrn=4774037132324&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774037132324&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774037132331&vrn=4774037132324&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774037132324&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774037132332&vrn=4774037132324&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774037132324&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774038112491&vrn=4774038112486&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774038112486&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774038112492&vrn=4774038112486&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774038112486&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774039117558&vrn=4774039117553&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774039117553&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774039117559&vrn=4774039117553&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774039117553&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774041119361&vrn=4774041119354&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774041119354&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774041119362&vrn=4774041119354&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774041119354&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774042124060&vrn=4774042124055&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774042124055&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774042124061&vrn=4774042124055&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774042124055&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774043127376&vrn=4774043127371&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774043127371&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774043127377&vrn=4774043127371&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774043127371&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774043127378&vrn=4774043127371&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774043127371&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774044122775&vrn=4774044122770&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774044122770&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774044122776&vrn=4774044122770&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774044122770&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774045124912&vrn=4774045124907&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774045124907&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774045124913&vrn=4774045124907&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774045124907&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774046124875&vrn=4774046124870&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774046124870&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774046124876&vrn=4774046124870&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774046124870&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774046124877&vrn=4774046124870&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774046124870&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774047135543&vrn=4774047135538&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774047135538&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774047135544&vrn=4774047135538&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774047135538&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774048101212&vrn=4774048101206&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774048101206&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774048101213&vrn=4774048101206&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774048101206&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774049118224&vrn=4774049118219&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774049118219&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774049118225&vrn=4774049118219&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774049118219&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774049118226&vrn=4774049118219&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774049118219&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774050137747&vrn=4774050137742&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774050137742&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774050137748&vrn=4774050137742&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774050137742&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774051128354&vrn=4774051128349&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774051128349&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774051128355&vrn=4774051128349&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774051128349&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774051128356&vrn=4774051128349&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774051128349&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774052120879&vrn=4774052120874&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774052120874&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774052120880&vrn=4774052120874&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774052120874&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774052120881&vrn=4774052120874&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774052120874&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774053124433&vrn=4774053124428&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774053124428&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774053124434&vrn=4774053124428&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774053124428&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774054119828&vrn=4774054119823&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774054119823&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774054119829&vrn=4774054119823&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774054119823&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774055127958&vrn=4774055127953&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774055127953&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774055127959&vrn=4774055127953&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774055127953&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774055127960&vrn=4774055127953&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774055127953&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774056135012&vrn=4774056135007&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774056135007&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774056135013&vrn=4774056135007&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774056135007&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774057146373&vrn=4774057146368&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774057146368&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774057146374&vrn=4774057146368&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774057146368&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774057146375&vrn=4774057146368&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774057146368&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774058116515&vrn=4774058116510&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774058116510&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774058116516&vrn=4774058116510&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774058116510&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774059126072&vrn=4774059126066&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774059126066&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774059126073&vrn=4774059126066&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774059126066&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774059126074&vrn=4774059126066&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774059126066&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774060123797&vrn=4774060123792&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774060123792&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774060123798&vrn=4774060123792&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774060123792&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774060123799&vrn=4774060123792&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774060123792&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774061104160&vrn=4774061104155&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774061104155&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774061104161&vrn=4774061104155&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774061104155&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774062117711&vrn=4774062117705&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774062117705&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774062117712&vrn=4774062117705&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774062117705&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774063117435&vrn=4774063117430&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774063117430&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774063117436&vrn=4774063117430&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774063117430&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774063117437&vrn=4774063117430&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774063117430&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774064162610&vrn=4774064162605&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774064162605&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774064162611&vrn=4774064162605&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774064162605&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774064162612&vrn=4774064162605&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774064162605&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774064162613&vrn=4774064162605&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774064162605&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774064162614&vrn=4774064162605&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774064162605&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774064162615&vrn=4774064162605&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774064162605&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774065109393&vrn=4774065109388&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774065109388&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774065109394&vrn=4774065109388&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774065109388&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774066120819&vrn=4774066120814&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774066120814&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774066120820&vrn=4774066120814&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774066120814&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774066120821&vrn=4774066120814&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774066120814&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774067136362&vrn=4774067136357&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774067136357&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774067136363&vrn=4774067136357&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774067136357&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774067136364&vrn=4774067136357&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774067136357&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=477406898052&vrn=477406898047&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=477406898047&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=477406898053&vrn=477406898047&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=477406898047&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774069123087&vrn=4774069123082&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774069123082&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774069123088&vrn=4774069123082&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774069123082&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774070141709&vrn=4774070141703&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774070141703&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774070141710&vrn=4774070141703&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774070141703&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774070141711&vrn=4774070141703&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774070141703&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774075155461&vrn=4774075155456&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774075155456&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774075155462&vrn=4774075155456&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774075155456&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774075155463&vrn=4774075155456&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774075155456&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774075155464&vrn=4774075155456&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774075155456&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=477407199571&vrn=477407199566&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=477407199566&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=477407199572&vrn=477407199566&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=477407199566&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774072168743&vrn=4774072168738&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774072168738&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774072168744&vrn=4774072168738&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774072168738&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774072168745&vrn=4774072168738&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774072168738&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774072168746&vrn=4774072168738&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774072168738&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774073136974&vrn=4774073136969&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774073136969&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774073136975&vrn=4774073136969&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774073136969&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774073136976&vrn=4774073136969&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774073136969&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774073136977&vrn=4774073136969&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774073136969&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774074138228&vrn=4774074138223&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774074138223&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774074138229&vrn=4774074138223&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774074138223&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774074138230&vrn=4774074138223&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774074138223&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774076147667&vrn=4774076147662&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774076147662&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774076147668&vrn=4774076147662&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774076147662&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774076147669&vrn=4774076147662&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774076147662&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774078126729&vrn=4774078126724&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774078126724&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774078126730&vrn=4774078126724&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774078126724&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774078126731&vrn=4774078126724&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774078126724&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774133140067&vrn=4774133140062&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774133140062&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774133140068&vrn=4774133140062&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774133140062&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774133140069&vrn=4774133140062&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774133140062&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774133140070&vrn=4774133140062&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774133140062&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774079115979&vrn=4774079115974&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774079115974&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774079115980&vrn=4774079115974&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774079115974&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774080151395&vrn=4774080151388&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774080151388&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774080151396&vrn=4774080151388&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774080151388&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774080151397&vrn=4774080151388&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774080151388&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774081117444&vrn=4774081117439&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774081117439&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774081117445&vrn=4774081117439&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774081117439&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774082121716&vrn=4774082121711&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774082121711&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774082121717&vrn=4774082121711&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774082121711&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774083117859&vrn=4774083117854&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774083117854&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774083117860&vrn=4774083117854&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774083117854&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774084142983&vrn=4774084142978&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774084142978&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774084142984&vrn=4774084142978&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774084142978&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774084142985&vrn=4774084142978&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774084142978&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774084142986&vrn=4774084142978&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774084142978&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774084142987&vrn=4774084142978&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774084142978&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774085133042&vrn=4774085133037&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774085133037&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774085133043&vrn=4774085133037&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774085133037&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774085133044&vrn=4774085133037&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774085133037&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774086132820&vrn=4774086132815&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774086132815&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774086132821&vrn=4774086132815&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774086132815&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774086132822&vrn=4774086132815&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774086132815&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774086132823&vrn=4774086132815&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774086132815&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774087133669&vrn=4774087133664&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774087133664&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774087133670&vrn=4774087133664&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774087133664&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774087133671&vrn=4774087133664&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774087133664&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774088104008&vrn=4774088104003&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774088104003&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774088104009&vrn=4774088104003&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774088104003&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774089166860&vrn=4774089166855&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774089166855&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774089166861&vrn=4774089166855&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774089166855&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774089166862&vrn=4774089166855&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774089166855&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774089166863&vrn=4774089166855&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774089166855&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774090106948&vrn=4774090106943&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774090106943&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774090106949&vrn=4774090106943&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774090106943&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774091144103&vrn=4774091144098&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774091144098&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774091144104&vrn=4774091144098&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774091144098&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774091144105&vrn=4774091144098&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774091144098&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774092132885&vrn=4774092132880&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774092132880&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774092132886&vrn=4774092132880&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774092132880&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774092132887&vrn=4774092132880&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774092132880&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774093155316&vrn=4774093155311&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774093155311&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774093155317&vrn=4774093155311&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774093155311&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774093155318&vrn=4774093155311&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774093155311&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774093155319&vrn=4774093155311&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774093155311&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774094208585&vrn=4774094208580&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774094208580&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774094208586&vrn=4774094208580&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774094208580&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774094208587&vrn=4774094208580&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774094208580&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774094208588&vrn=4774094208580&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774094208580&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774095105546&vrn=4774095105540&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774095105540&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774095105547&vrn=4774095105540&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774095105540&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774095105548&vrn=4774095105540&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774095105540&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774096109360&vrn=4774096109355&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774096109355&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774096109361&vrn=4774096109355&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774096109355&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774097131294&vrn=4774097131289&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774097131289&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774097131295&vrn=4774097131289&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774097131289&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774097131296&vrn=4774097131289&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774097131289&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774098124008&vrn=4774098124003&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774098124003&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774098124009&vrn=4774098124003&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774098124003&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774099129527&vrn=4774099129522&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774099129522&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774099129528&vrn=4774099129522&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774099129522&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774100121502&vrn=4774100121491&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774100121491&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774100121503&vrn=4774100121491&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774100121491&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774101124055&vrn=4774101124049&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774101124049&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774101124056&vrn=4774101124049&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774101124049&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774101124057&vrn=4774101124049&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774101124049&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774102126767&vrn=4774102126762&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774102126762&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774102126768&vrn=4774102126762&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774102126762&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774102126769&vrn=4774102126762&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774102126762&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774102126770&vrn=4774102126762&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774102126762&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774103137928&vrn=4774103137923&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774103137923&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774103137929&vrn=4774103137923&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774103137923&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774103137930&vrn=4774103137923&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774103137923&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774104139807&vrn=4774104139802&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774104139802&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774104139808&vrn=4774104139802&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774104139802&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774104139809&vrn=4774104139802&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774104139802&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774105118557&vrn=4774105118552&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774105118552&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774105118558&vrn=4774105118552&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774105118552&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774106140518&vrn=4774106140513&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774106140513&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774106140519&vrn=4774106140513&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774106140513&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774107126877&vrn=4774107126838&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774107126838&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774107126878&vrn=4774107126838&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774107126838&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774108120442&vrn=4774108120437&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774108120437&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774108120443&vrn=4774108120437&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774108120437&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774109136061&vrn=4774109136056&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774109136056&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774109136062&vrn=4774109136056&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774109136056&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774109136063&vrn=4774109136056&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774109136056&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774110123928&vrn=4774110123923&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774110123923&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774110123929&vrn=4774110123923&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774110123923&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774110123930&vrn=4774110123923&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774110123923&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774111157563&vrn=4774111157558&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774111157558&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774111157564&vrn=4774111157558&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774111157558&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774111157565&vrn=4774111157558&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774111157558&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774112171733&vrn=4774112171728&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774112171728&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774112171734&vrn=4774112171728&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774112171728&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774112171735&vrn=4774112171728&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774112171728&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774113144726&vrn=4774113144720&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774113144720&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774113144727&vrn=4774113144720&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774113144720&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774113144728&vrn=4774113144720&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774113144720&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774114127804&vrn=4774114127799&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774114127799&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774114127805&vrn=4774114127799&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774114127799&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774115129121&vrn=4774115129116&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774115129116&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774115129122&vrn=4774115129116&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774115129116&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774116133746&vrn=4774116133741&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774116133741&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774116133747&vrn=4774116133741&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774116133741&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774116133748&vrn=4774116133741&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774116133741&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774117116892&vrn=4774117116887&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774117116887&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774117116893&vrn=4774117116887&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774117116887&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774119135574&vrn=4774119135569&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774119135569&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774119135575&vrn=4774119135569&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774119135569&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774119135576&vrn=4774119135569&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774119135569&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774120127371&vrn=4774120127366&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774120127366&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774120127372&vrn=4774120127366&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774120127366&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774121143326&vrn=4774121143320&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774121143320&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774121143327&vrn=4774121143320&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774121143320&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774122139335&vrn=4774122139330&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774122139330&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774122139336&vrn=4774122139330&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774122139330&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774123126129&vrn=4774123126124&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774123126124&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774123126130&vrn=4774123126124&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774123126124&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774124156039&vrn=4774124156034&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774124156034&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774124156040&vrn=4774124156034&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774124156034&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774124156041&vrn=4774124156034&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774124156034&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774125144985&vrn=4774125144980&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774125144980&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774125144986&vrn=4774125144980&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774125144980&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774125144987&vrn=4774125144980&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774125144980&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774128137520&vrn=4774128137515&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774128137515&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774128137521&vrn=4774128137515&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774128137515&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774129130843&vrn=4774129130838&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774129130838&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774129130844&vrn=4774129130838&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774129130838&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774130122833&vrn=4774130122828&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774130122828&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774130122834&vrn=4774130122828&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774130122828&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774131149993&vrn=4774131149988&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774131149988&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774131149994&vrn=4774131149988&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774131149988&report_mode=null'
        'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774131149995&vrn=4774131149988&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774131149988&report_mode=null'

    )
    csv = 'name,declined,parties,won\n'
    file = open('info2017.csv', 'w')
    district = 1
    for link_mid in links:
        # show_progress_bar(district, mandates=125)
        district += 1
        file.write(csv)
        csv = parse_page_info(links)
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
        '4774004151548',
        '4774004151547',
        '4774004151549',
        '4774005159149',
        '4774005159150',
        '4774005159151',
        '4774006133202',
        '4774006133203',
        '4774006133204',
        '4774007117789',
        '4774007117790',
        '4774008112814',
        '4774008112815',
        '4774010120042',
        '4774010120043',
        '4774010120044',
        '4774009134024',
        '4774009134025',
        '4774009134026',
        '4774011164122',
        '4774011164123',
        '4774011164124',
        '4774013126105',
        '4774013126106',
        '4774014127356',
        '4774014127357',
        '4774014127358',
        '4774015125479',
        '4774015125480',
        '4774015125481',
        '4774016123407',
        '4774016123408',
        '4774017109310',
        '4774017109311',
        '4774018119471',
        '4774018119472',
        '4774018119473',
        '4774018119474',
        '4774019123064',
        '4774019123065',
        '4774020142944',
        '4774020142945',
        '4774022146204',
        '4774022146205',
        '4774024151060',
        '4774024151061',
        '4774025130167',
        '4774025130168',
        '4774026116759',
        '4774026116760',
        '4774027138657',
        '4774027138658',
        '4774027138659',
        '4774028131168',
        '4774028131169',
        '4774029131732',
        '4774029131733',
        '4774030117556',
        '4774030117557',
        '4774031150415',
        '4774031150416',
        '4774033139896',
        '4774033139897',
        '4774035127413',
        '4774035127414',
        '4774040125484',
        '4774040125485',
        '4774032129795',
        '4774032129796',
        '4774034121516',
        '4774034121517',
        '4774037132330',
        '4774037132331',
        '4774037132332',
        '4774038112491',
        '4774038112492',
        '4774039117558',
        '4774039117559',
        '4774041119361',
        '4774041119362',
        '4774042124060',
        '4774042124061',
        '4774043127376',
        '4774043127377',
        '4774044122775',
        '4774044122776',
        '4774045124912',
        '4774045124913',
        '4774046124875',
        '4774046124876',
        '4774046124877',
        '4774047135543',
        '4774047135544',
        '4774048101212',
        '4774048101213',
        '4774049118224',
        '4774049118225',
        '4774049118226',
        '4774050137747',
        '4774050137748',
        '4774051128354',
        '4774051128355',
        '4774051128356',
        '4774052120879',
        '4774052120880',
        '4774052120881',
        '4774053124433',
        '4774053124434',
        '4774054119828',
        '4774054119829',
        '4774055127958',
        '4774055127959',
        '4774055127960',
        '4774056135012',
        '4774056135013',
        '4774057146373',
        '4774057146374',
        '4774057146375',
        '4774058116515',
        '4774058116516',
        '4774059126072',
        '4774059126073',
        '4774059126074',
        '4774060123797',
        '4774060123798',
        '4774060123799',
        '4774061104160',
        '4774061104161',
        '4774062117711',
        '4774062117712',
        '4774063117435',
        '4774063117436',
        '4774063117437',
        '4774064162610',
        '4774064162611',
        '4774064162612',
        '4774064162613',
        '4774064162614',
        '4774064162615',
        '4774065109393',
        '4774065109394',
        '4774066120819',
        '4774066120820',
        '4774066120821',
        '4774067136362',
        '4774067136363',
        '4774067136364',
        '477406898052',
        '477406898053',
        '4774069123087',
        '4774069123088',
        '4774070141709',
        '4774070141710',
        '4774070141711',
        '4774075155461',
        '4774075155462',
        '4774075155463',
        '4774075155464',
        '477407199571',
        '477407199572',
        '4774072168743',
        '4774072168744',
        '4774072168745',
        '4774072168746',
        '4774073136974',
        '4774073136975',
        '4774073136976',
        '4774073136977',
        '4774074138228',
        '4774074138229',
        '4774074138230',
        '4774076147667',
        '4774076147668',
        '4774076147669',
        '4774078126729',
        '4774078126730',
        '4774078126731',
        '4774133140067',
        '4774133140068',
        '4774133140069',
        '4774133140070',
        '4774079115979',
        '4774079115980',
        '4774080151395',
        '4774080151396',
        '4774080151397',
        '4774081117444',
        '4774081117445',
        '4774082121716',
        '4774082121717',
        '4774083117859',
        '4774083117860',
        '4774084142983',
        '4774084142984',
        '4774084142985',
        '4774084142986',
        '4774084142987',
        '4774085133042',
        '4774085133043',
        '4774085133044',
        '4774086132820',
        '4774086132821',
        '4774086132822',
        '4774086132823',
        '4774087133669',
        '4774087133670',
        '4774087133671',
        '4774088104008',
        '4774088104009',
        '4774089166860',
        '4774089166861',
        '4774089166862',
        '4774089166863',
        '4774090106948',
        '4774090106949',
        '4774091144103',
        '4774091144104',
        '4774091144105',
        '4774092132885',
        '4774092132886',
        '4774092132887',
        '4774093155316',
        '4774093155317',
        '4774093155318',
        '4774093155319',
        '4774094208585',
        '4774094208586',
        '4774094208587',
        '4774094208588',
        '4774095105546',
        '4774095105547',
        '4774095105548',
        '4774096109360',
        '4774096109361',
        '4774097131294',
        '4774097131295',
        '4774097131296',
        '4774098124008',
        '4774098124009',
        '4774099129527',
        '4774099129528',
        '4774100121502',
        '4774100121503',
        '4774101124055',
        '4774101124056',
        '4774101124057',
        '4774102126767',
        '4774102126768',
        '4774102126769',
        '4774102126770',
        '4774103137928',
        '4774103137929',
        '4774103137930',
        '4774104139807',
        '4774104139808',
        '4774104139809',
        '4774105118557',
        '4774105118558',
        '4774106140518',
        '4774106140519',
        '4774107126877',
        '4774107126878',
        '4774108120442',
        '4774108120443',
        '4774109136061',
        '4774109136062',
        '4774109136063',
        '4774110123928',
        '4774110123929',
        '4774110123930',
        '4774111157563',
        '4774111157564',
        '4774111157565',
        '4774112171733',
        '4774112171734',
        '4774112171735',
        '4774113144726',
        '4774113144727',
        '4774113144728',
        '4774114127804',
        '4774114127805',
        '4774115129121',
        '4774115129122',
        '4774116133746',
        '4774116133747',
        '4774116133748',
        '4774117116892',
        '4774117116893',
        '4774119135574',
        '4774119135575',
        '4774119135576',
        '4774120127371',
        '4774120127372',
        '4774121143326',
        '4774121143327',
        '4774122139335',
        '4774122139336',
        '4774123126129',
        '4774123126130',
        '4774124156039',
        '4774124156040',
        '4774125144985',
        '4774125144986',
        '4774125144987',
        '4774128137520',
        '4774128137521',
        '4774129130843',
        '4774129130844',
        '4774130122833',
        '4774130122834',
        '4774131149993',
        '4774131149994',
        '4774131149995'
    )
    csv = 'name,district,mandate,votes,potential_voters,inside_voters,early_voters,outside_voters,attendance,early,outside\n'
    file = open('data2017.csv', 'w')
    district = 1
    for link_mid in link_mids:
        # show_progress_bar(district, mandates=125)
        file.write(csv)
        csv = parse_page_results(link_left + link_mid + link_right)
        district += 1
        # time.sleep(9)
    file.write(csv)
    file.close()

