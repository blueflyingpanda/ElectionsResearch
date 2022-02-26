import sys
from parser_election2017 import parse_election_results2017, parse_election_info2017
from parser_election2017 import browser as browser2017
from parser_election2022 import parse_election2022
from os import path
import pandas as pd


def convert_parties_to_numbers():
    file = open('info2017.csv', 'r')
    text = file.read()
    file2 = open('info2017.csv', 'w')
    text = text.replace('Самовыдвижение', '0')
    text = text.replace('МОСКОВСКОЕ ГОРОДСКОЕ ОТДЕЛЕНИЕ Политической партии КОММУНИСТИЧЕСКАЯ ПАРТИЯ КОММУНИСТЫ РОССИИ', '3')
    text = text.replace('Московское городское отделение Всероссийской политической партии "ПАРТИЯ РОСТА"', '6')
    text = text.replace('Региональное отделение в городе Москве Политической партии Гражданская Платформа', '11')
    text = text.replace('Региональное отделение политической партии "Российская объединенная демократическая партия "ЯБЛОКО" в городе Москве', '9')
    text = text.replace('Московское городское отделение Политической партии ЛДПР - Либерально-демократической партии России', '5')
    text = text.replace('Региональное отделение Политической партии СПРАВЕДЛИВАЯ РОССИЯ в городе Москве', '8')
    text = text.replace('МОСКОВСКОЕ ГОРОДСКОЕ ОТДЕЛЕНИЕ политической партии "КОММУНИСТИЧЕСКАЯ ПАРТИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ"', '4')
    text = text.replace('Региональное отделение Общественной организации Всероссийская политическая партия Гражданская Сила в г. Москве', '1')
    text = text.replace('Московское городское региональное отделение Всероссийской политической партии "ЕДИНАЯ РОССИЯ"', '10')
    text = text.replace('Региональное отделение в городе Москве Политической партии "Российская экологическая партия "Зелёные"', '2')
    text = text.replace('Региональное отделение ВСЕРОССИЙСКОЙ ПОЛИТИЧЕСКОЙ ПАРТИИ "РОДИНА" в городе Москве', '7')
    text = text.replace('Региональное отделение в городе Москве Всероссийской политической партии Социал-демократическая партия России', '12')
    text = text.replace('Московское городское отделение ПОЛИТИЧЕСКОЙ ПАРТИИ "АЛЬЯНС ЗЕЛЕНЫХ"', '13')
    text = text.replace('Московское городское региональное отделение политической партии "ПАТРИОТЫ РОССИИ', '14')
    text = text.replace('Региональное отделение в городе Москва Политической партии "Национальный курс"', '15')
    text = text.replace('Региональное отделение в городе Москве Всероссийской политической партии "Партия Великое Отечество"', '16')
    text = text.replace('Региональное отделение в Москве Политической партии "Партия народной свободы (ПАРНАС)"', '17')
    text = text.replace('Региональное отделение в Москве Политической партии "Партия народной свободы" (ПАРНАС)', '17')
    text = text.replace('Региональное отделение Всероссийской политической партии "Союз Труда" в городе Москве', '18')
    text = text.replace('Региональное отделение политической партии "Объединенная партия людей ограниченной трудоспособности России" в городе Москве', '19')
    text = text.replace('Московское городское региональное отделение Общероссийской политической партии "НАРОД ПРОТИВ КОРРУПЦИИ"', '20')
    text = text.replace('Региональное отделение в городе Москве Всероссийской политической партии "Партия Возрождения Села"', '21')
    file2.write(text)
    file.close()
    file2.close()


def main():
    if len(sys.argv) != 2:
        print('should be one additional argument')
        exit(1)
    if sys.argv[1] == '2017':
        if not path.isfile('data2017.csv'):
            parse_election_results2017()
        if not path.isfile('info2017.csv'):
            parse_election_info2017()
        convert_parties_to_numbers()
        # JUST FOR KIckS
        # browser2017.get('http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=4774001137464&vrn=4774001137457&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=4774001137457&report_mode=null')
        # html_source = browser2017.page_source
        # df = pd.read_html(html_source, attrs = {'class': 'table-bordered table-sm dataTable no-footer'}, encoding='utf-8')
        # print(df)
        # df[0].to_csv('kicks.csv')
        browser2017.close()
    # elif sys.argv[1] == '2022':
        # if not path.isfile('data2022.csv'):
        #     parse_election_results2022()
        # if not path.isfile('info2022.csv'):
        #     parse_election_info2022()
        # browser2022.close()
    else:
        print('Invalid year, should 2017 or 2022 year')




if __name__ == '__main__':
    main()