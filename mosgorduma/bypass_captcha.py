import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def main():
    browser = webdriver.Chrome()
    link_left = 'http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1&tvd='
    link_right = '&vrn=27720002327736&prver=0&pronetvd=null&region=77&sub_region=77&type=424&report_mode=null'
    link_mids = (
        '27720002327741',
        '27720002327747',
        '27720002327752',
        '27720002327756',
        '27720002327760',
        '27720002327764',
        '27720002327769',
        '27720002327774',
        '27720002327779',
        '27720002327785',
        '27720002327789',
        '27720002327793',
        '27720002327797',
        '27720002327801',
        '27720002327807',
        '27720002327811',
        '27720002327815',
        '27720002327819',
        '27720002327824',
        '27720002327828',
        '27720002327834',
        '27720002327837',
        '27720002327841',
        '27720002327845',
        '27720002327850',
        '27720002327853',
        '27720002327857',
        '27720002327860',
        '27720002327864',
        '27720002327868',
        '27720002327871',
        '27720002327875',
        '27720002327880',
        '27720002327883',
        '27720002327887',
        '27720002327890',
        '27720002327894',
        '27720002327899',
        '27720002327905',
        '27720002327911',
        '27720002327915',
        '27720002327919',
        '27720002327923',
        '27720002327927',
        '27720002327932'
    )
    i = 0
    while i < len(link_mids):
        browser.get(link_left + link_mids[i] + link_right)
        time.sleep(5)
        html_content = browser.page_source
        if '<meta charset="UTF-8">' in html_content:
            captcha = input('please enter captcha and press enter\n')
            form = browser.find_element_by_id('captcha')
            form.send_keys(captcha)
            button = browser.find_element_by_id('send')
            button.click()
            continue
        print('page', i)
        i += 1
    browser.close()

if __name__ == '__main__':
    main()