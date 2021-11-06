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


def extract_mandate(line):
    start = line.find(',')
    return int(line[start + 1: line.find(',', start + 1)])


def form_clean_data(election_number):
    """gather together all data and save it in clean_data"""
    data = open(f'data{election_number}', 'r')
    info = open(f'info{election_number}', 'r')
    hand = open(f'info{election_number}', 'r')
    parties = open(f'parties{election_number}', 'r')
    clean = open(f'clean_data{election_number}', 'w')
    single_mandate = 0
    i = next(info)
    for d, h, p in zip(data, hand, parties):
        if extract_mandate(d) > single_mandate:
            single_mandate += 1
            i = next(info)
        clean.write(f'{d},{i},{h},{p}\n')


def main():
    if len(sys.argv) != 2:
        print('election not specified!')
        exit(1)
    if sys.argv[1] == '2014':
        start_time = time.time()
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