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
options.headless = False
driver = webdriver.Firefox(options = options, executable_path = gecko_path)

###########################################################################
#################### Scraping links to property offers ####################
###########################################################################

url = 'https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/warszawa/'
driver.get(url)
time.sleep(1)

# Clicking cookies consent
button = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
button.click()

# The site is displaying property offers in a table; getting links to properties by tr of class=wrap
regexp = re.compile(r'http')

def find_links1(property_links, length):
    links = driver.find_elements(By.XPATH, '//tr[@class="wrap"]/td/div/table/tbody/tr[1]/td[1]/a')
    print("* trying first xpath to link *")
    for element in links:
        property_links.append(element.get_attribute('href'))
    if length == len(property_links):
        links = driver.find_elements(By.XPATH, '//div[@class="css-19ucd76"]/a')
        print("* trying second xpath to link *")
        for element in links:
            element = element.get_attribute('href')
            if regexp.search(element):
                property_links.append(element)
            else:
                property_links.append('https://www.olx.pl' + element)
    return property_links

# Defining function used for scraping more pages
def find_links2(i, property_links, length):
    url = 'https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/warszawa/?page=' + str(i)
    driver.get(url)
    time.sleep(1)
    property_links = find_links1(property_links, length)
    time.sleep(1)
    return property_links

property_links = []
length = 0
property_links = find_links1(property_links, length)
length = len(property_links)
print(length)

# If bool parameter is set to True we limit links to 100
i = 2
if limit:
    while length < 100:
        property_links = find_links2(i, property_links, length)
        i = i + 1
        length = len(property_links)
        print(length)
    property_links = list(set(property_links))[:100]
else:
    while i < 26:
        property_links = find_links2(i, property_links, length)
        i = i + 1
        length = len(property_links)

print('Number of property offers: ', len(property_links))

###########################################################################
################## Scraping information on each property ##################
###########################################################################

# d = pd.DataFrame({'name':[], 'price':[], 'price_m2':[], 'map':[]})
# m2
# rooms
# floor
# rent

# Clicking cookies consent
url = 'https://www.otodom.pl/'
driver.get(url)
time.sleep(1)
button = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
button.click()

regexp = re.compile(r'otodom')

# for url in property_links:
    # driver.get(url)
url = property_links[95]

driver.get(url)
time.sleep(1)

if regexp.search(url):
    print('* otodom scraping is at work *')
    name = driver.find_element(By.XPATH, '//h1').get_attribute("innerHTML").splitlines()[0]
    price = driver.find_element(By.XPATH, '//header/strong').get_attribute("innerHTML").splitlines()[0]
    price = price.split('zł', 1)[0]
    price = re.sub(" ", "", price)
    price_m2 = driver.find_element(By.XPATH, '//div[@aria-label="Cena za metr kwadratowy"]').get_attribute("innerHTML").splitlines()[0]
    price_m2 = price_m2.split('zł', 1)[0]
    price_m2 = re.sub(" ", "", price_m2)
    # m2 = driver.find_element(By.XPATH, '//div[@aria-label="Powierzchnia"/div[2]]/div').get_attribute("innerHTML").splitlines()[0]
    # rooms = driver.find_element(By.XPATH, '//div[@aria-label="Liczba pokoi"/div[2]]/div').get_attribute("innerHTML").splitlines()[0]
    # floor = driver.find_element(By.XPATH, '//div[@aria-label="Piętro"/div[2]]/div').get_attribute("innerHTML").splitlines()[0]
    # rent = driver.find_element(By.XPATH, '//div[@aria-label="Czynsz"/div[2]]/div').get_attribute("innerHTML").splitlines()[0]
    # description = driver.find_element(By.XPATH, '//main/div[3]/div[2]/section[2]/div/div/p').get_attribute("innerHTML").splitlines()[0]
    map = driver.find_element(By.XPATH, '//a[@aria-label="Adres"]').get_attribute("innerHTML").splitlines()[0]
    map = map.split('>', 4)[4]
    
    

else:
    print('* olx site scraping is at work *')
    name = driver.find_element(By.XPATH, '//h1').get_attribute("innerHTML").splitlines()[0]
    price = driver.find_element(By.XPATH, '//h3').get_attribute("innerHTML").splitlines()[0]
    price = price.split('zł', 1)[0]
    price = re.sub(" ", "", price)
    price_m2 = driver.find_element(By.XPATH, '//html/body/div[1]/div[1]/div[3]/div[3]/div[1]/div[2]/ul/li[2]/p').get_attribute("innerHTML").splitlines()[0]
    price_m2 = price_m2.split(' ', 4)[3]


    # key_words = ''
    # keywords = driver.find_elements(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[3]/div[1]/div[2]/ul/li/p')
    # regexp3 = re.compile(r'span')
    # for key in keywords:
    #     if regexp3.search(key.get_attribute("innerHTML").splitlines()[0]):
    #         key_words = key_words + driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[3]/div[1]/div[2]/ul/li[1]/p/span').get_attribute("innerHTML").splitlines()[0] + ' '
    #     else:
    #         key_words = key_words + key.get_attribute("innerHTML").splitlines()[0] + ' '

    map = 'Warszawa, ' + driver.find_element(By.XPATH, '//html/body/div[1]/div[1]/div[3]/div[3]/div[2]/div[2]/div/section/div[1]/div/p[1]/span').text
    
    # try:
    #     description = driver.find_element(By.XPATH, '//div[@class="css-g5mtbi-Text"]').get_attribute("innerHTML").splitlines()[0]
    # except:
    #     description = driver.find_element(By.XPATH, '//div[@class="css-g5mtbi-Text"]').get_attribute("innerHTML").splitlines()[0]

print(name)
print(price)
print(price_m2)
# print(m2)
# print(rooms)
# print(floor)
# print(rent)
print(map)



    