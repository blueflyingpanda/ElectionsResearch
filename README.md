# Данные о выборах в Мосгордуму 2019
### финальный датасет в двух эксемплярах находится в файлах full_data.csv и full_data.xls

### поля датасета:

**name** -> ФИО кандидата <br/> 
**party** -> партия кандидата <br/> 

0 - Самовыдвижение <br/> 
1 - Гражданская сила <br/>
2 - Зеленые <br/>
3 - Коммунисты России <br/>
4 - КПРФ <br/>
5 - ЛДПР <br/>
6 - Партия Роста <br/>
7 - Родина <br/>
8 - Справедливая Россия <br/>
9 - Яблоко <br/>

**smart_vote** -> была ли поддержка умного голосования для этого кандидата 0 - не поддержан 1 - поддержан<br/>
**joined_united_rus** -> кандидат присоединился к Единой России не прошел - -1, не присоединился - 0, присоединился - 1 <br/>
**single_mandate** -> номер округа <br/>
**votes** -> кол-во голосов, которые набрал кандидат <br/>
**potential_voters** -> кол-во потенциальных голосующих, числящихся за округом <br/>
**inside_voters** -> кол-во голосовавших на участке <br/>
**early_voters** -> кол-во проголосовавших заранее <br/>
**outside_voters** -> кол-во проголосовавших не на участке <br/>
**attendance** -> явка в процентах <br/>
**early** -> процент проголосовавших заранее от общего числа проголосовавших <br/>
**outside** -> процент проголосовавших не на участке от общего числа проголосовавших <br/>
**won** -> статус кандидата 1 - победил, 0 - проиграл <br/>
**declined** -> кол-во отказов <br/>
**state_employee** -> является ли кандидат бюджетником 1 - да, 0 - нет, -1 - от партий <br/>
**affiliation** -> отношение к власти спойлер - 0, административный 1, неадминистративный 2 <br/>

## ВАЖНО!

Данные в датасетах *.csv и *.xls отличаются <br/>
*.csv оптмизирован для взаимодействия с python и pandas <br/>
*.xls приведен в читаемый для человека вид. <br/>

### все изменения в *.xls:

1 - нет первой колонки c id, которая нужна pandas-у <br/>
2 - в колонке **party** цифра меняется на названия партии, чтобы не приходилось, каждый раз соотносить <br/>
3 - в колонке **smart_vote** 0 меняется на "нет", 1 меняется на "да" <br/>
4 - в колонке **joined_united_rus** -1 меняется на "не прошел", 0 меняется на "не присоединился", 1 меняется на "присоединился" <br/>
5 - в колонке **won** 0 меняется на "проиграл", 1 меняется на "победил" <br/>
6 - в колонке **state_employee** 1 меняется на "да", 0 меняется на "нет", -1 меняется на "от партий" <br/>
7 - в колонке **affiliation** 0 меняется на "спойлер", 1 меняется на "административный", 2 меняется на "неадминистративный" <br/>

### можно еще изменить названия колонок, но мы решили, что так датасет будет неузнаваемым

## как собирались данные
![ЦИК РФ](data:image/jpeg;base64,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)

### parser_election7_results.py

Программа парсит [Сводные таблицы результатов выборов депутатов Московской городской Думы седьмого созыва по
одномандатному округу.](http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=27720002327741&vrn=27720002327736&prver=0&pronetvd=null&region=77&sub_region=77&type=424&report_mode=null) <br/>
Результаты сохраняются в файл **data.csv** <br/>
Поробнее в _docstrings_ <br/>

### parser_election7_info.py

Программа парсит [Программа парсит сведения о кандидатах выборов депутатов Московской городской Думы седьмого созыва по
одномандатному округу.](http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=27720002327741&vrn=27720002327736&prver=0&pronetvd=null&region=77&sub_region=77&type=424&report_mode=null) <br/>
Результаты сохраняются в файл **info.csv** <br/>
Эта информация помогает посчитать количество отказов в регистрации в каждом округе <br/>
Поробнее в _docstrings_ <br/>

### mandates_to_districts_to_uiks.py

Программа парсит **mandates_to_districts_to_uiks.txt** и создает **mandates_to_districts_to_uiks.csv** <br/>
Чтобы установить связь между округами, районами и УИК-ами <br/>
Поробнее в _docstrings_ <br/>

### violation_map.py

Программа парсит данные [Карты Нарушений на выборах 8 сентября 2019](https://www.kartanarusheniy.org/2019-09-08/s/3928382754) <br/>
если в сообщении о нарушении не указан уик - сообщение не учитывается <br/>
Результаты сохраняются в файл **violation_map.csv** <br/>
Поробнее в _docstrings_ <br/>

### clean_data.csv

Файл который собирается вручную из прошлых *.csv файлов <br/>

### affiliation.py

На основе данных собранных с помощью **parser_election7_info.py** и **parser_election7_results.py** и части данных,
собранных вручную в файле **clean_data.csv**, высчитывается еще одна колонка affiliation со значениями _(спойлер - 0,
административный 1, неадминистративный 2)_, которая высчитывает по [алгоритму](https://miro.com/app/board/o9J_lqoY7Ww=/)
принадлежность кандидата <br/>
Эта колонка добавляется в clean_data.csv и сохраняется в файле full_data.csv <br/>

### test.py

Тестирует affiliation в full_data.csv <br/>
который получили из affiliation.py <br/>


## requirments.txt 

В файле requirments.txt прописаны все зависимости для python <br/>
`pip install -r requirements.txt`