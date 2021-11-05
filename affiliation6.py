import affiliation as af
import pandas as pd

def if_won(df, n , affiliation_array):
    if df['won'][n] == False:
        if df['ur_affiliated'][n] == 1:
            affiliation_array.append(0)
        else:
            affiliation_array.append(2)
    else:
        if df['joined_united_rus'][n] == 1:
            affiliation_array.append(1)
        else:
            affiliation_array.append(2)

# def candidate_ur(df, n):
#     single_mandate_df = df[df['single_mandate'] == df['single_mandate'][n]]
#     for i in single_mandate_df.index:
#         if single_mandate_df['party'][i] == 10:
#             return True
#     return False



def main():
    parliament_parties = {4, 5, 8}
    df = pd.read_csv('clean_data6.csv')
    affiliation_array = []
    for n in df.index:
        if df['party'][n] == 10:
            affiliation_array.append(1)
        else:
            if df['party'][n] == 9 or df['party'][n] in parliament_parties:
                affiliation_array.append(2)
            else:
                if df['potential_voters'][n] * 0.03 > df['votes'][n]:
                    affiliation_array.append(0)
                else:
                    if_won(df, n, affiliation_array)
    df['affiliation'] = affiliation_array
    df.to_csv('full_data6.csv', sep=',', encoding='utf-8', index=False)


if __name__ == '__main__':
    main()