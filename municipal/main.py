import sys
from parser_election2017 import parse_election_results2017, parse_election_info2017
from parser_election2017 import browser as browser2017
from parser_election2022 import parse_election2022
from os import path
import pandas as pd


def main():
    if len(sys.argv) != 2:
        print('should be one additional argument')
        exit(1)
    if sys.argv[1] == '2017':
        if not path.isfile('data2017.csv'):
            parse_election_results2017()
        if not path.isfile('info2017.csv'):
            parse_election_info2017()
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