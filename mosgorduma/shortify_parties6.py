def main():
    file = open('parties6.csv', 'r')
    file2 = open('parties6short.csv', 'w')
    text = file.read()
    text = text.replace('Самовыдвижение', '0')
    text = text.replace('Региональное отделение в городе Москве Политической партии Гражданская Платформа', '11')
    text = text.replace('Региональное отделение Политической партии Российская объединенная демократическая партия ЯБЛОКО в городе Москве', '9')
    text = text.replace('Московское городское отделение политической партии Либерально-демократическая партия России', '5')
    text = text.replace('Региональное отделение Политической партии СПРАВЕДЛИВАЯ РОССИЯ в городе Москве', '8')
    text = text.replace('МОСКОВСКОЕ ГОРОДСКОЕ ОТДЕЛЕНИЕ политической партии КОММУНИСТИЧЕСКАЯ ПАРТИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ', '4')
    text = text.replace('Региональное отделение Всероссийской политической партии Гражданская Сила в Москве', '1')
    text = text.replace('Московское городское региональное отделение Всероссийской политической партии ЕДИНАЯ РОССИЯ', '10')
    text = text.replace('Региональное отделение в городе Москве Политической партии Российская экологическая партия Зеленые', '2')
    text = text.replace('Региональное отделение ВСЕРОССИЙСКОЙ ПОЛИТИЧЕСКОЙ ПАРТИИ РОДИНА в городе Москве', '7')
    text = text.replace('Региональное отделение в городе Москве Всероссийской политической партии Социал-демократическая партия России', '12')
    file2.write(text)
    file.close()
    file2.close()

if __name__ == '__main__':
    main()
