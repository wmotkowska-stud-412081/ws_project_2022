##scrapping OLX site with beautiful soup

from urllib import request
from bs4 import BeautifulSoup as BS
import re
import pandas as pd

print('--')
print('It will take about 2,5 minutes for this program to finish')
print('--')

url='https://www.olx.pl/d/nieruchomosci/mieszkania/sprzedaz/warszawa/'
html = request.urlopen(url)
bs = BS(html.read(), 'html.parser')

# Setting up a boolean parameter "limit". If it is True, links are limited to 100
limit = True

i = 2
x = 25  # here we can choose how many olx main pages we want to scrap later. Setting it as 25, because there are as many pages now

# as  next pages cannot be accessed in a different way (by scrapping only 1,2,3 and lat page can be accessed),
# they had to be collected more manually, by iterating number of a page in the end of the url and adding it to "first_links"

first_links = []
first_links.append(url)
while i <= x:
    first_links.append('https://www.olx.pl/d/nieruchomosci/mieszkania/sprzedaz/warszawa/?page='+str(i))
    i += 1

# in the next step: links to offers are scrapped using links from first_links. They are selected by their class
# they are also limited to 100 if boolean is true as requested in the assignment

olx_links = []
# below is the limit of number of pages from first_links can be easily changed. Setting it as 100 as requested in assignment
a = 100
regex_otodom = re.compile(r'otodom')

for link in first_links:
#    print(link)
    html = request.urlopen(link)
    bs = BS(html.read(), 'html.parser')
    tags = bs.find_all('div', attrs={'class': 'css-19ucd76'})
    for tag in tags:
    # below if limit is true: it is made sure that not more than 100 links (a=100) is being used
        if limit:
            if len(olx_links) < a:
                temporary_links2 = []
                try:
# adding scrapped links to a temporary table
                    temporary_links2.append('https://www.olx.pl' + tag.a['href'])
                    check = str(temporary_links2)
                except:
                    0
# adding links to the olx_links on a condition, that they are not otodom pages
                if not regex_otodom.search(check):
                    olx_links.extend(temporary_links2)
# if limit boolean is not true, there can be more than 100 links
        else:
            temporary_links2 = []
            try:
                temporary_links2.append('https://www.olx.pl' + tag.a['href'])
            except:
                0
            olx_links.extend(temporary_links2)

# printing number of links to show that the right amount is used
print('Those are the used links:', olx_links)
print('Number or property offers:', len(olx_links))


## now we will scrap information from stored in olx_links links and save information in a table

# creating an empty table, that will be filled, once the info is scrapped
table = pd.DataFrame({'name': [], 'price': [], 'price_m2': [],'m2': [],'rooms': [],'floor': [],'url': []})


# name and price could be found by h1 and h3 attributes
# for the rest information, there needed first to be a table scrapped, and later this table was splited into
# m2, price_m2, floors, rooms, but only if those details exist on the page
# after scrapping all variables, they are saved in a table
for olx_link in olx_links:
    html = request.urlopen(olx_link)
    bs = BS(html.read(), 'html.parser')

    try:
        name = bs.find('h1').text
    except:
        name = ''

    try:
        price = bs.find('h3').text
    except:
        price = ''
# some variables needed to be split,do they only contain certain information, to make it easier to analyse later
    price = price.split('zł', 1)[0]
    price = re.sub(" ", "", price)

    try:
        details = bs.find_all('p', {'class': 'css-xl6fe0-Text eu5v0x0'})
    except:
        details = ''

    for element in details:
        detail = element.text
        if "Powierzchnia:" in detail:
            m2 = detail.split(' ', 2)[1]
        if "Poziom:" in detail:
            floor = detail.split(' ', 1)[1]
        if "Liczba pokoi:" in detail:
            rooms = detail.split(' ', 3)[2]
        if "Cena za m" in detail:
            price_m2 = detail.split(' ', 4)[3]


    information = ({'name': name, 'price': price, 'price_m2': price_m2, 'm2': m2, 'rooms': rooms, 'floor': floor, 'url': olx_link})
# below, scrapped information are added to a table
    table = table.append(information, ignore_index=True)

# program will print the whole created table
print('This is the received table:')
print(table)

# program will save collected data as a csv file
table.to_csv('data_bs.csv')
