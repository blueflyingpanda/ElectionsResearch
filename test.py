"""
Тестирует affiliation в full_data.csv
который получили из affiliation.py
"""

import pandas as pd

df = pd.read_csv('full_data.csv')
voc = {0: 'спойлер', 1: 'адм', 2: 'не адм'}


def test(i, expected):  # i - индекс в таблице, expected - предполагаемое значение affiliation
    got = df['affiliation'][i]
    if got == expected:
        print(i, 'passed')
    else:
        print(i, 'failed', '->', df['name'][i].split()[0], 'expected:', voc[expected], 'got:', voc[got])


def main():
    test(219, 1)  # Свиридов
    test(222, 1)  # Касамара
    test(114, 0)  # Тарасов Антон
    test(74, 0)   # Андреева Александра Александровна
    test(147, 2)  # Юнеман


if __name__ == '__main__':
    main()
