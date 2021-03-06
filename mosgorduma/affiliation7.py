"""На основе данных собранных с помощью parser_election7_info.py и parser_election7_results.py и части данных
собранных вручную в файле clean_data7.csv, высчитывается еще одна колонка affiliation со значениями(спойлер - 0,
административный 1, неадминистративный 2), которая высчитывает по алгоритму
принадлежность кандидата (ознакомиться с древом решений можно здесь https://miro.com/app/board/o9J_lqoY7Ww=/) Эта
колонка добавляется в clean_data7.csv и сохраняется в файле full_data7.csv

Изначальные поля clean_data7.csv:
name -> ФИО кандидата

party -> партия кандидата
0 - Самовыдвижение
1 - Гражданская сила
2 - Зеленые
3 - Коммунисты России
4 - КПРФ
5 - ЛДПР
6 - Партия Роста
7 - Родина
8 - Справедливая Россия
9 - Яблоко

smart_vote -> была ли поддержка умного голосования для этого кандидата
joined_united_rus -> кандидат присоединился к Единой России -1 - не прошел, не присоединился - 0, присоединился - 1
single_mandate -> номер округа
votes -> кол-во голосов, которые набрал кандидат
potential_voters -> кол-во потенциальных голосующих, числящихся за округом
inside_voters -> кол-во голосовавших на участке
early_voters -> кол-во проголосовавших заранее
outside_voters -> кол-во проголосовавших не на участке
attendance -> явка в процентах
early -> процент проголосовавших заранее от общего числа проголосовавших
outside -> процент проголосовавших не на участке от общего числа проголосовавших
won -> статус кандидата 1 - победил, 0 - проиграл
declined -> кол-во отказов
state_employee -> является ли кандидат бюджетником 1 - да, 0 - нет, -1 - null
"""

import pandas as pd


def modified_fuzzy_search(name1, name2):
    name1 = name1[0:name1.find(' ')]
    name2 = name2[0:name2.find(' ')]
    length = min(len(name1), len(name2))
    error = length // 4
    for i in range(length):
        if name1[i] != name2[i]:
            error -= 1
            if error < 0:
                return False
    return True


def has_alike_name(df, i) -> bool:
    single_mandate_df = df[df['single_mandate'] == df['single_mandate'][i]]
    for x in single_mandate_df.index:
        if single_mandate_df['name'][x] != df['name'][i] and single_mandate_df['name'][x][0] == df['name'][i][0] and \
                modified_fuzzy_search(single_mandate_df['name'][x], df['name'][i]):
            return True
    return False


def is_only_independent(df, i) -> bool:
    single_mandate_df = df[df['single_mandate'] == df['single_mandate'][i]]
    for x in single_mandate_df.index:
        if single_mandate_df['name'][x] != df['name'][i] and single_mandate_df['party'][x] == 0:
            return False
    return True


def main():
    parliament_parties = {4, 5, 8}
    df = pd.read_csv('clean_data7.csv')
    affiliation_array = []
    for i in df.index:
        if df['smart_vote'][i] == 1:
            affiliation_array.append(2)
        else:
            if has_alike_name(df, i) and df['party'][i] != 4 and df['party'][i] != 8 and df['party'][i] != 9:
                affiliation_array.append(0)
            else:
                if df['party'][i] in parliament_parties:
                    affiliation_array.append(2)
                else:
                    if df['potential_voters'][i] * 0.03 > df['votes'][i]:
                        affiliation_array.append(0)
                    else:
                        if df['party'][i] == 0:
                            if is_only_independent(df, i):
                                affiliation_array.append(1)
                            else:
                                if df['won'][i] == 1:
                                    if df['joined_united_rus'][i] == 1:
                                        affiliation_array.append(1)
                                    elif df['joined_united_rus'][i] == 0:
                                        affiliation_array.append(2)
                                    else:
                                        raise Exception(df['name'][i])  # -1 там, где должно быть 0 или 1
                                else:
                                    if df['state_employee'][i] == 1:
                                        affiliation_array.append(1)
                                    else:
                                        affiliation_array.append(2)
                        else:
                            if df['party'][i] == 3:
                                affiliation_array.append(0)
                            else:
                                affiliation_array.append(2)
    df['affiliation'] = affiliation_array
    df.to_csv('full_data7.csv', sep=',', encoding='utf-8', index = False)


if __name__ == '__main__':
    main()
