import sys
from parser_election2017 import parse_election_results2017, parse_election_info2017
from parser_election2017 import browser as browser2017
from parser_election2022 import parse_election2022


def main():
    if len(sys.argv) != 2:
        print('should be one additional argument')
        exit(1)
    if sys.argv[1] == '2017':
        # parse_election_results2017()
        parse_election_info2017()
        browser2017.close()
    elif sys.argv[1] == '2022':
        parse_election2022()
    else:
        print('Invalid year, should 2017 or 2022 year')




if __name__ == '__main__':
    main()