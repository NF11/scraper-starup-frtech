import os
import time
from random import randint

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains

from utilis_function import _french_login

links = []
SCROLL_PAUSE_TIME = 5
founders = None
founders_name = []
founders_role = []
founders_linkedin = []
twitter = " "
facebook = " "
linkedin = " "
index = 0
url = input('insert path : ')
csv = str(input('insert name file to save :')) + '.csv'
dr = webdriver.Chrome(executable_path='driver/chromedriver')
dr.maximize_window()
dr.get(str(url))
_french_login(dr)
time.sleep(10)
r = BeautifulSoup(dr.page_source, 'html.parser')
all_num = r.find('span', class_='fadein').text.split(" ")

all_num = all_num[1].replace(',', '')
i = 0
print('start scrap company\'s url ')
while True:
    my_liste = dr.find_element_by_class_name('virtual-list.table-list')
    my_listes = BeautifulSoup(my_liste.parent.page_source, 'html.parser') \
        .find('div', class_='virtual-list table-list').find_all('a')
    for url in my_listes:
        if url['href'].find('/companies/') > -1 and url['href'] not in links:
            links.append(url['href'])
            i += 1
            print(str(i) + ' / ' + str(all_num))
    print('---------------------------------------------------------')
    try:
        target = dr.find_element_by_xpath('//*[@id="list-map-list"]/div/div[2]/div/div[21]')
        actions = ActionChains(dr)
        actions.move_to_element(target)
        actions.perform()
        dr.implicitly_wait(1000)
        time.sleep(SCROLL_PAUSE_TIME)
    except NoSuchElementException:
        pass
    if i == int(all_num):
        dr.close()
        break
csv_path = str(os.getcwd()) + str(csv)
row_num = 0
with open(csv, 'w') as f:
    f.write('nom, description, address, site, linkedin, twitter, facebook, année de lancement, employees, '
            'Growth stage, valorisation, funding, '
            'founder/1/nom, founder/1/poste, founder/1/linkedin,'
            'founder/2/nom, founder/2/poste, founder/2/linkedin,'
            'founder/3/nom, founder/3/poste, founder/3/linkedin,'
            'founder/4/nom, founder/4/poste, founder/4/linkedin,'
            '\n')
    rows_num = len(links)
    for row in links:
        row_num += 1
        print('start scarp :' + str(row_num) + ' / ' + str(rows_num) + ' ' + str(row))
        dr = webdriver.Chrome()
        dr.get('https://ecosystem.lafrenchtech.com' + str(row))
        dr.implicitly_wait(100)
        soup = BeautifulSoup(dr.page_source, 'html.parser')
        name = soup.find('h1', class_='name')
        description = soup.find('div', class_='tagline')
        address = \
            soup.find('div', attrs={'class': 'company-locations'})
        site = soup.find('a', class_='item-details-info__url')
        utls = soup.find('div', class_='resource-urls company-tags__resource-urls')
        company_info = soup.find('div', class_='layout-container company-overview')
        date = company_info.find('div', class_='field launch-date').find('div', class_='description')
        employee = company_info.find('div', class_='field employees').find('div', class_='description')
        stage = company_info.find('div', class_='field growth-stage').find('div', class_='description')
        value = company_info.find('div', class_='field firm-valuation').find('div', class_='description') \
            .find('span', class_='valuation__value') if company_info.find('div',
                                                                          class_='field firm-valuation') is not None else None
        funding = soup.find('tfoot', class_='simple-table__footer')
        dr.find_element_by_css_selector("a.underlined-tab:nth-child(4)").click()
        dr.implicitly_wait(100)
        try:
            founders = dr.find_element_by_class_name('team-member.team-member-founder.vbox')
            founders = BeautifulSoup(founders.parent.page_source, 'html.parser') \
                .find_all('div', class_='team-member team-member-founder vbox')
        except NoSuchElementException:
            pass
        if founders is not None:
            for item in founders:
                # text
                founders_name.append(item.find('div', class_="info").find('a', class_="name"))
                # text
                founders_role.append(item.find('div', class_="info").find('span', class_="team-member__job-title"))
                # ['href']
                founders_linkedin.append(
                    item.find('div', class_="info").find('a', class_="team-member__linkedin hbox vertical-center"))

        name = " " if name is None else name.text
        description = " " if description is None else description.text
        site = " " if site is None else str(site['href'])
        date = " " if date is None else date.text
        employee = " " if employee is None else employee.find('a').text
        stage = " " if stage is None else stage.find('a').text
        value = " " if value is None else value.text
        funding = " " if funding is None else funding.find('tr').find_all('td')[1].find('span',
                                                                                        class_='tooltip-target').text

        if address is None:
            address = " "
        else:
            address = address.find('meta', attrs={'itemprop': 'address'})
            if address is None:
                address = " "
            else:
                address = str(address['content'])

        if utls is not None:
            allA = utls.find_all('a')
            for a in allA:
                if a is not None:
                    if str(a['href']).find('twitter') > -1:
                        twitter = str(a['href'])
                    if str(a['href']).find('linkedin') > -1:
                        linkedin = str(a['href'])
                    if str(a['href']).find('facebook') > -1:
                        facebook = str(a['href'])

        text = name.replace(',', " ") + ',' + description.replace(',', " ") + ',' + address.replace(',', " ") \
               + ',' + site + ',' + linkedin + ',' + twitter + ',' + facebook + ',' + date + ',' + employee + ',' \
               + stage + ',' + value + ',' + funding
        for fou in founders_name:
            text += ',' + fou.text.replace(',', " ")
            text += "," + " " if founders_role[index] is None else ',' + founders_role[index].text.replace(',', " ")
            text += "," + " " if founders_linkedin[index] is None else ',' + founders_linkedin[index]['href'].replace(
                ',', " ")
            index += 1
            if index == 3:
                break
        f.write(text + '\n')

        time.sleep(randint(2, 5))
        founders_name = []
        founders_role = []
        founders_linkedin = []
        twitter = " "
        facebook = " "
        linkedin = " "
        founders = None
        index = 0
        soup = ""
        dr.close()
print('finish ')
