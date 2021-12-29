import pandas as pd
import sys

def get_computed_data6(lst):
    print(len(lst))
    prev_max = -1
    maximum = -1
    spoilers = 0
    opposition = 0
    adm_voters = -1
    for l in lst:
        if prev_max < l['voters_percent']:
            prev_max = l['voters_percent']
            if maximum < prev_max:
                prev_max, maximum = maximum, prev_max
        if l['affiliation'] == 1:
            adm_voters = l['voters_percent']
        elif l['affiliation'] == 0:
            spoilers += 1
        elif l['affiliation'] == 2:
            opposition += 1
    return spoilers, opposition, adm_voters, prev_max

def get_computed_data7(lst):
    print(len(lst))
    spoilers = 0
    opposition = 0
    adm_voters = -1
    smart_voters = -1
    for l in lst:
        if l['smart_vote'] == 1:
            smart_voters = l['voters_percent']
        if l['affiliation'] == 1:
            adm_voters = l['voters_percent']
        elif l['affiliation'] == 0:
            spoilers += 1
        elif l['affiliation'] == 2:
            opposition += 1
    return spoilers, opposition, adm_voters, smart_voters

def get_data_for_analysis6(df):
    with open('data_for_analysis6.csv', 'w') as data:
        data.write(f'single_mandate,attendance,early,outside,adm_voters,second_voters,spoilers,opposition,declined\n')
        attendance = df.iloc[0]['attendance']
        outside = df.iloc[0]['outside']
        early = df.iloc[0]['early']
        declined = df.iloc[0]['declined']
        mandate = 1
        tmp_lst = []
        for _, row in df.iterrows():
            if row['single_mandate'] > mandate:
                spoilers, opposition, adm_voters, second_voters = get_computed_data6(tmp_lst)
                data.write(f'{mandate},{attendance},{early},{outside},{adm_voters},{second_voters},{spoilers},{opposition},{declined}\n')
                attendance = row['attendance']
                outside = row['outside']
                early = row['early']
                declined = row['declined']
                mandate += 1
                tmp_lst = []
            tmp_lst.append({
                             "voters_percent": (row['votes'] * 100) / row['potential_voters'],
                             "affiliation": row['affiliation']})
        spoilers, opposition, adm_voters, second_voters = get_computed_data6(tmp_lst)
        data.write(f'{mandate},{attendance},{early},{outside},{adm_voters},{second_voters},{spoilers},{opposition},{declined}\n')



def get_data_for_analysis7(df):
    with open('data_for_analysis7.csv', 'w') as data:
        data.write(f'single_mandate,attendance,early,outside,adm_voters,smart_voters,spoilers,opposition,declined\n')
        attendance = df.iloc[0]['attendance']
        outside = df.iloc[0]['outside']
        early = df.iloc[0]['early']
        declined = df.iloc[0]['declined']
        mandate = 1
        tmp_lst = []
        for _, row in df.iterrows():
            if row['single_mandate'] > mandate:
                spoilers, opposition, adm_voters, smart_voters = get_computed_data7(tmp_lst)
                data.write(f'{mandate},{attendance},{early},{outside},{adm_voters},{smart_voters},{spoilers},{opposition},{declined}\n')
                attendance = row['attendance']
                outside = row['outside']
                early = row['early']
                declined = row['declined']
                mandate += 1
                tmp_lst = []
            tmp_lst.append({
                "smart_vote": row['smart_vote'],
                "voters_percent": (row['votes'] * 100) / row['potential_voters'],
                "affiliation": row['affiliation']})
        spoilers, opposition, adm_voters, smart_voters = get_computed_data7(tmp_lst)
        data.write(f'{mandate},{attendance},{early},{outside},{adm_voters},{smart_voters},{spoilers},{opposition},{declined}\n')

def main():
    if len(sys.argv) != 2:
        print('election not specified!')
        exit(1)
    if sys.argv[1] == '2014':
        get_data_for_analysis6(pd.read_csv('full_data6.csv'))
    else:
        get_data_for_analysis7(pd.read_csv('full_data7.csv'))

if __name__ == '__main__':
    main()
