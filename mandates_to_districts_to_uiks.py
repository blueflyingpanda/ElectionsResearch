"""
Программа парсит mandates_to_districts_to_uiks.txt и создает mandates_to_districts_to_uiks.csv с полями
mandate -> номер округа
district -> название района
uik -> номер уика
Эти данные потом используются для подсчета нарушений в округах (violation_map.py)
"""


def main():

    with open('mandates_to_districts_to_uiks.csv', 'w') as csv_file:
        csv_file.write('mandate,district,uik\n')
        with open('mandates_to_districts_to_uiks.txt', 'r') as txt_file:
            for line in txt_file:
                if line[0] == 'О' and line[1] == 'д':
                    mandate = line[line.find('№') + 2:len(line) - 1]
                elif line[0] == 'У' and line[1] == 'И':
                    line = line[line.find('№') + 1:]
                    csv_file.write(mandate + ',' + district + ',' + line)
                else:
                    district = line[:len(line) - 1]


if __name__ == '__main__':
    main()
