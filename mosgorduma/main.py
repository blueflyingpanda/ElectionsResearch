import sys
import time
import affiliation6
import affiliation7
import parser_election6_parties
import parser_election7_parties
import shortify_parties6
import shortify_parties7
import parser_election6_results
import parser_election7_results
import parser_election6_info
import parser_election7_info
import mandates_to_districts_to_uiks
import violation_map
from pathlib import Path


def extract_mandate(line):
    start = line.find(',')
    return int(line[start + 1: line.find(',', start + 1)])


def form_clean_data(election_number):
    """gather together all data and save it in clean_data"""
    data = open(f'data{election_number}.csv', 'r')
    info = open(f'info{election_number}.csv', 'r')
    hand = open(f'hand_data{election_number}.csv', 'r')
    parties = open(f'parties{election_number}short.csv', 'r')
    clean = open(f'clean_data{election_number}.csv', 'w')
    single_mandate = 0
    i = next(info)
    i = i.split(',')[1]
    first = False
    for d, h, p in zip(data, hand, parties):
        if first and extract_mandate(d) > single_mandate:
            single_mandate += 1
            i = next(info)
            i = i.split(',')[1]
        first = True
        d = d.strip('\n')
        i = i.strip('\n')
        h = h.strip('\n')
        p = p.strip('\n')
        p = p.split(',')[1]
        clean.write(f'{d},{i},{h},{p}\n')
    data.close()
    info.close()
    hand.close()
    parties.close()
    clean.close()


def main():
    if len(sys.argv) != 2:
        print('election not specified!')
        exit(1)
    if sys.argv[1] == '2014':
        start_time = time.time()
        data = Path('data6.csv')
        info = Path('info6.csv')
        parties = Path('parties6.csv')
        if not data.is_file() or not info.is_file() or not parties.is_file():
            parser_election6_results.main()
            print("DATA --- %s seconds ---" % (time.time() - start_time))
            parser_election6_info.main()
            print("INFO --- %s seconds ---" % (time.time() - start_time))
            parser_election6_parties.main()
        shortify_parties6.main()
        print("PARTIES --- %s seconds ---" % (time.time() - start_time))
        form_clean_data(6)
        affiliation6.main()
        print("TOTAL --- %s seconds ---" % (time.time() - start_time))
    elif sys.argv[1] == '2019':
        start_time = time.time()
        data = Path('data7.csv')
        info = Path('info7.csv')
        parties = Path('parties7.csv')
        if not data.is_file() or not info.is_file() or not parties.is_file():
            parser_election7_results.main()
            print("DATA --- %s seconds ---" % (time.time() - start_time))
            parser_election7_info.main()
            print("INFO --- %s seconds ---" % (time.time() - start_time))
            parser_election7_parties.main()
        shortify_parties7.main()
        print("PARTIES --- %s seconds ---" % (time.time() - start_time))
        # mandates_to_districts_to_uiks.main()
        # violation_map.main()
        form_clean_data(7)
        affiliation7.main()
        print("TOTAL --- %s seconds ---" % (time.time() - start_time))
    else:
        print('wrong year!')
        exit(1)


if __name__ == '__main__':
    main()