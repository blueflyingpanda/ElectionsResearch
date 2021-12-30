### кратко:

Данная программа скрэйпит, парсит, очищает, обогащает данные о выборах в Мосгордуму за 2014 и 2019 годы согласно [алгоритмам](https://miro.com/app/board/o9J_lqoY7Ww=/?invite_link_id=822385482583). После этого данные собираются в датасеты [full_data6.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/full_data6.csv) для 2014 года и [full_data7.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/full_data7.csv) для 2019 года. За один запуск создается один датасет, в зависимости от выбранного года.

Часть данных анализировались с помощью отдельного скрипта [data_for_analysis.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/data_for_analysis.py), чтобы продолжить анализ в Excel. Результат работы этого скрипта в сохранятеся либо в [data_for_analysis6.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/data_for_analysis6.csv) для 2014 года, либо в [data_for_analysis7.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/data_for_analysis7.csv) для 2019 года.

_**цифра 6 всегда означает выборы 2014 года (шестой созыв) <br/>
цифра 7 всегда означает выборы 2019 года (седьмой созыв)**_

---

### поля датасетов full_data:

**name** -> ФИО кандидата <br/>
**single_mandate** -> номер округа <br/>
**votes** -> количество голосов, которые набрал кандидат <br/>
**potential_voters** -> количество голосовавших на избирательных участках <br/>
**inside_voters** -> количество избирателей в округе <br/>
**early_voters** -> количество проголосовавших досрочно <br/>
**outside_voters** -> количество проголосовавших вне помещения для голосования <br/>
**attendance** -> явка в процентах <br/>
**early** -> процент проголосовавших досрочно от общего числа проголосовавших <br/>
**outside** -> процент проголосовавших вне помещения для голосования от общего числа проголосовавших <br/>
**won** -> статус кандидата, 1 - победил, 0 - проиграл <br/>
**declined** -> количество отказов в регистрации кандидата/выбыл после регистрации <br/>
**joined_united_rus** -> кандидат присоединился к фракции "Единой России" или "Моя Москва" в Мосгордуме после избрания. Не присоединился - 0, присоединился - 1 <br/>
**ur_affiliated** -> !!! <br/>
**smart_vote** -> была ли поддержка "Умного голосования" для этого кандидата, 0 - не поддержан, 1 - поддержан <br/>
**state_employee** -> является ли кандидат бюджетником, 1 - да, 0 - нет, -1 - от партий <br/>
**affiliation** -> отношение к власти, спойлер - 0, административный 1, оппозиционный 2 <br/>
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
10 - Единая Россия <br/>
11 - Гражданская Платформа <br/>
12 - Социал-демократическая партия России <br/>

### поля датасетов data_for_analysis:

**single_mandate** -> номер округа <br/>
**attendance** -> явка в процентах <br/>
**early** -> процент проголосовавших досрочно от общего числа проголосовавших <br/>
**outside** -> процент проголосовавших вне помещения для голосования от общего числа проголосовавших <br/>
**adm_voters** -> процент проголосовавших за административного кандидата от общего числа проголосовавших <br/>
**smart_voters** -> процент проголосовавших за кандидата от умного голосования от общего числа проголосовавших <br/>
**second_voters** -> процент проголосовавших за самого близкого к победе кандидата от общего числа проголосовавших <br/>
**spoilers** -> процент спойлеров от всех зарегистрированных кандидатов <br/>
**opposition** -> процент оппозиционых кандидатов от всех зарегистрированных кандидатов <br/>
**declined** -> процент отказов в регистрации от всех, кто подавался <br/>

---

### как собираются данные

[parser_election6_results.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/parser_election6_results.py)

Парсит [сводные таблицы результатов выборов депутатов Московской городской Думы шестого созыва по
одномандатному округу.](http://www.moscow-city.vybory.izbirkom.ru/region/region/moscow-city?action=show&root=1&tvd=27720001539819&vrn=27720001539308&region=77&global=null&sub_region=77&prver=0&pronetvd=null&cuiknum=null&type=424) <br/>
Результаты сохраняются в файл [data6.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/data6.csv) <br/>
Поробнее в _docstrings_ <br/>

[parser_election6_info.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/parser_election6_info.py)

Парсит [сведения о кандидатах выборов депутатов Московской городской Думы шестого созыва по
одномандатному округу.](http://www.moscow-city.vybory.izbirkom.ru/region/region/moscow-city?action=show&root=1&tvd=27720001539819&vrn=27720001539308&region=77&global=&sub_region=77&prver=0&pronetvd=null&vibid=27720001539308&type=220) <br/>
Результаты сохраняются в файл [info6.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/info6.csv) <br/>
Эта информация помогает посчитать количество отказов в регистрации в каждом округе <br/>
Поробнее в _docstrings_ <br/>

[parser_election6_parties.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/parser_election6_parties.py)

Парсит [сведения о партиях выборов депутатов Московской городской Думы шестого созыва по
одномандатному округу.](http://www.moscow-city.vybory.izbirkom.ru/region/region/moscow-city?action=show&root=1&tvd=27720001539819&vrn=27720001539308&region=77&global=&sub_region=77&prver=0&pronetvd=null&vibid=27720001539308&type=220) <br/>
Результаты сохраняются в файл [parties6.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/parties6.csv) <br/>
Эта информация помогает посчитать количество отказов в регистрации в каждом округе <br/>
Поробнее в _docstrings_ <br/>

[shortify_parties6.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/shortify_parties6.py)

Присваивает названию партии число и сохраняет в файл [parties6short.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/parties6short.csv)

[affiliation6.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/affiliation6.py)

На основе данных собранных с помощью [parser_election6_results.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/parser_election6_results.py), [parser_election6_info.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/parser_election6_info.py), [parser_election6_parties.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/parser_election6_parties.py) и части данных,
собранных вручную с сайта [Мосгордумы](https://duma.mos.ru/ru/) в файле [hand_data6.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/hand_data6.csv), в функции [form_clean_data](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/main.py#L23-L50) формируется файл [clean_data6.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/clean_data6.csv). [affiliation6.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/affiliation6.py) высчитывает еще одну колонку **affiliation** со значениями _спойлер - 0,
административный 1, неадминистративный 2_, которая высчитывает по [алгоритмам](https://miro.com/app/board/o9J_lqoY7Ww=/?invite_link_id=822385482583)
принадлежность кандидата <br/>
Эта колонка добавляется в [clean_data6.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/clean_data6.csv) и сохраняется в файле [full_data6.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/full_data6.csv) <br/>

---
[parser_election7_results.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/parser_election7_results.py)

Парсит [сводные таблицы результатов выборов депутатов Московской городской Думы седьмого созыва по
одномандатному округу.](http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=27720002327741&vrn=27720002327736&prver=0&pronetvd=null&region=77&sub_region=77&type=424&report_mode=null) <br/>
Результаты сохраняются в файл [data7.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/data7.csv) <br/>
Поробнее в _docstrings_ <br/>

[parser_election7_info.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/parser_election7_info.py)

Программа парсит [Программа парсит сведения о кандидатах выборов депутатов Московской городской Думы седьмого созыва по
одномандатному округу.](http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=27720002327741&vrn=27720002327736&prver=0&pronetvd=null&region=77&sub_region=77&type=424&report_mode=null) <br/>
Результаты сохраняются в файл [info7.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/info7.csv) <br/>
Эта информация помогает посчитать количество отказов в регистрации в каждом округе <br/>
Поробнее в _docstrings_ <br/>

[parser_election7_parties.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/parser_election7_parties.py)

Парсит [сведения о партиях выборов депутатов Московской городской Думы седьмого созыва по
одномандатному округу.](http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd=27720002327741&vrn=27720002327736&prver=0&pronetvd=null&region=77&sub_region=77&type=220&vibid=27720002327736&report_mode=null) <br/>
Результаты сохраняются в файл [parties7.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/parties7.csv) <br/>
Эта информация помогает посчитать количество отказов в регистрации в каждом округе <br/>
Поробнее в _docstrings_ <br/>

[shortify_parties7.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/shortify_parties7.py)

Присваивает названию партии число и сохраняет в файл [parties7short.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/parties7short.csv)

[affiliation7.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/affiliation7.py)

На основе данных собранных с помощью [parser_election7_results.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/parser_election7_results.py), [parser_election7_info.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/parser_election7_info.py), [parser_election7_parties.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/parser_election7_parties.py) и части данных,
собранных вручную с сайта [Мосгордумы](https://duma.mos.ru/ru/) и [Умного голосования](http://web.archive.org/web/20190829180251/https:/msk.vote/) в файле [hand_data7.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/hand_data7.csv), в функции [form_clean_data](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/main.py#L23-L50) формируется файл [clean_data7.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/clean_data7.csv). [affiliation7.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/affiliation7.py) высчитывает еще одну колонку **affiliation** со значениями _спойлер - 0,
административный 1, неадминистративный 2_, которая высчитывает по [алгоритмам](https://miro.com/app/board/o9J_lqoY7Ww=/?invite_link_id=822385482583)
принадлежность кандидата <br/>
Эта колонка добавляется в [clean_data7.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/clean_data7.csv) и сохраняется в файле [full_data7.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/full_data7.csv) <br/>

---

[main.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/main.py)

Точка входа в программу

### как пользоваться на MacOSX и Linux:
0. перейти в директорию с программой, если репозиторий созранен на рабочем столе и называется ElectionsResearch, то <br/> `cd ~/Desktop/ElectionsResearch/mosgorduma`
0. при условии, что установлен Питон версии не ниже 3.6 установить зависимости `pip install -r requirements.txt`
1. если хотите собрать данные самостоятельно - удалите все .csv файлы кроме собранных вручную [hand_data6.csv] и [hand_data7.csv] <br/> `mv hand_data6.csv ..` <br/> `mv hand_data7.csv ..` <br/> `rm -rf *.csv` <br/> `mv ../hand_data6.csv .` <br/> `mv ../hand_data7.csv .`
2. запустить программу <br/> `python3 main.py 2014` или `python3 main.py 2019`

---

### пока не используется:

[mandates_to_districts_to_uiks.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/mandates_to_districts_to_uiks.py)

Парсит [mandates_to_districts_to_uiks.txt](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/mandates_to_districts_to_uiks.txt) и создает [mandates_to_districts_to_uiks.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/mandates_to_districts_to_uiks.csv) <br/>
Чтобы установить связь между округами, районами и УИК-ами <br/>
Поробнее в _docstrings_ <br/>

[violation_map.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/violation_map.py)

Парсит данные [Карты Нарушений на выборах 8 сентября 2019](https://www.kartanarusheniy.org/2019-09-08/s/3928382754) <br/>
если в сообщении о нарушении не указан уик - сообщение не учитывается <br/>
Результаты сохраняются в файл [violation_map.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/violation_map.csv) <br/>
Поробнее в _docstrings_ <br/>

[bypass_captcha.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/bypass_captcha.py)

Попытка обойти капчу на сайте ЦИК

[progress_bar.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/progress_bar.py)

Тестировался только на Unix-like системах, чтобы отобразить progress bar процесса скрейпинга

### собиралось руками:
 
[hand_data6.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/hand_data6.csv) для 2014 года и [hand_data7.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/hand_data7.csvhttps://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/hand_data7.csv) для 2019 года

### тесты:

[test.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/test.py)

Тестирует **affiliation** в [full_data6.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/full_data6.csv) и [full_data7.csv](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/full_data7.csv) <br/>
который получили из [affiliation6.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/affiliation6.py) и [affiliation7.py](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/mosgorduma/affiliation7.py) <br/>

### зависимости:

В файле [requirments.txt](https://github.com/blueflyingpanda/ElectionsResearch/blob/main/requirments.txt) прописаны все зависимости для python <br/>
