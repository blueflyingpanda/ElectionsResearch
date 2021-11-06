"""
Тестирует affiliation в full_data7.csv
который получили из affiliation7.py
"""

import pandas as pd

df = pd.read_csv('full_data7.csv')
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
    test(19, 1)   # Бабаян
    test(44, 0)   # Дашкевич
    test(78, 1)   # Молев
    test(33, 2)   # Беседина
    test(84, 2)   # Марусенко
    test(123, 1)  # Стебенкова
    test(143, 0)  # Викулин
    test(163, 2)  # Смирнов
    test(181, 1)  # Шарапова
    test(223, 0)  # Конев
    test(190, 1)  # Головченко


if __name__ == '__main__':
    main()
