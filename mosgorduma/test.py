"""
Тестирует affiliation в full_data7.csv
который получили из affiliation7.py
"""

import pandas as pd

df = pd.read_csv('full_data7.csv')
voc = {0: 'спойлер', 1: 'адм', 2: 'не адм'}


def test(i, expected):  # i - индекс в таблице, expected - предполагаемое значение affiliation
    i -= 2
    got = df['affiliation'][i]
    if got == expected:
        print(i, 'passed')
    else:
        print(i, 'failed', '->', df['name'][i].split()[0], 'expected:', voc[expected], 'got:', voc[got])


def main():
    test(220, 1)  # Свиридов
    test(223, 1)  # Касамара
    test(116, 0)  # Тарасов Антон
    test(76, 0)   # Андреева Александра Александровна
    test(149, 2)  # Юнеман
    test(21, 1)   # Бабаян
    test(46, 0)   # Дашкевич
    test(80, 1)   # Молев
    test(35, 2)   # Беседина
    test(86, 2)   # Марусенко
    test(125, 1)  # Стебенкова
    test(144, 0)  # Викулин
    test(165, 2)  # Смирнов
    test(183, 1)  # Шарапова
    test(224, 0)  # Конев
    test(195, 1)  # Головченко


if __name__ == '__main__':
    main()
