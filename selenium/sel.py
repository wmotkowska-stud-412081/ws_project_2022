###########################################################################
##################### Scraping OLX site with selenium #####################
###########################################################################

from operator import length_hint
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re

# Setting up a boolean parameter limiting the number of pages.
limit = True

# Setting up and conneting to site using selenium tools
gecko_path = 'C:/Users/weron/anaconda3/Library/geckodriver'
options = webdriver.firefox.options.Options()
options.headless = True
driver = webdriver.Firefox(options = options, executable_path = gecko_path)

###########################################################################
#################### Scraping links to property offers ####################
###########################################################################

# Accessing the website
url = 'https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/warszawa/'
driver.get(url)
time.sleep(1)

# Clicking cookies consent
button = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
button.click()

# The site is displaying property offers in a table; getting links to properties by tr of class=wrap
regexp = re.compile(r'http')
regexp2 = re.compile(r'otodom')

# Defining function used for scraping links 
def find_links1(property_links, length):
    links = driver.find_elements(By.XPATH, '//tr[@class="wrap"]/td/div/table/tbody/tr[1]/td[1]/a')
    
    print("* trying first xpath to link *")
    for element in links:
        if not regexp2.search(element.get_attribute('href')):
            property_links.append(element.get_attribute('href'))
        
    if length == len(property_links):
        links = driver.find_elements(By.XPATH, '//div[@class="css-19ucd76"]/a')
        print("* trying second xpath to link *")
        for element in links:
            if limit and len(property_links) >= 100:
                return property_links
            else:
                element = element.get_attribute('href')
                if not regexp2.search(element) and element not in property_links:
                    if regexp.search(element):
                        property_links.append(element)
                    else:
                        property_links.append('https://www.olx.pl' + element)
    return property_links

# Defining function used for accessing page to scrap links
def find_links2(i, property_links, length):
    url = 'https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/warszawa/?page=' + str(i)
    driver.get(url)
    time.sleep(2)
    property_links = find_links1(property_links, length)
    return property_links

# Defining parameters
property_links = []
length = 0

# Scraping first page for links to properties
property_links = find_links1(property_links, length)
length = len(property_links)
print(length)

# Scraping more pages, if bool parameter is set to True we limit links to 100
i = 2
if limit:
    while length < 100:
        property_links = find_links2(i, property_links, length)
        i = i + 1
        length = len(property_links)
        print(length)
else:
    while i < 26:
        property_links = find_links2(i, property_links, length)
        i = i + 1
        length = len(property_links)

print('Number of property offers: ', len(property_links))

###########################################################################
################## Scraping information on each property ##################
###########################################################################

# Defining dataframe to store information on properties
d = pd.DataFrame({'name':[], 'price':[], 'price_m2':[], 'm2':[], 'rooms':[], 'floor':[], 'map':[], 'url':[]})

# Scraping every link for information by accessing tags and cleaning the obtainedinformation
for url in property_links:
    driver.get(url)
    time.sleep(15)

    print('* olx site scraping is at work *')
    name = driver.find_element(By.XPATH, '//h1').get_attribute("innerHTML").splitlines()[0]
    price = driver.find_element(By.XPATH, '//h3').get_attribute("innerHTML").splitlines()[0]
    price = price.split('zł', 1)[0]
    price = re.sub(" ", "", price)
    map = 'Warszawa, ' + driver.find_element(By.XPATH, '//html/body/div[1]/div[1]/div[3]/div[3]/div[2]/div[2]/div/section/div[1]/div/p[1]/span').text
    details = driver.find_elements(By.XPATH, '//p[@class="css-xl6fe0-Text eu5v0x0"]')

    for element in details:
        element = element.text
        if "Powierzchnia" in element:
            m2 = element.split(' ', 2)[1]
            m2 = re.sub(",", ".", m2)
        if "Poziom" in element:
            floor = element.split(' ', 1)[1]
        if "Liczba pokoi" in element:
            rooms = element.split(' ', 3)[2]
        if "Cena za" in element:
            price_m2 = element.split(' ', 4)[3]

    property = {'name':name, 'price':price, 'price_m2':price_m2, 'm2':m2, 'rooms':rooms, 'floor':floor, 'map':map, 'url':url}
    d = d.append(property, ignore_index = True)

# Saving results to csv
d.to_csv('data/data_selenium.csv')
