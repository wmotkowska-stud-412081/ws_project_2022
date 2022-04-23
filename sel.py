###########################################################################
##################### Scraping OLX site with selenium #####################
###########################################################################

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
time.sleep(5)

# Clicking cookies consent
button = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
button.click()
time.sleep(5)

# The site is displaying property offers in a table; getting links to properties by tr of class=wrap
def find_links1(property_links):
    links = driver.find_elements(By.XPATH, '//tr[@class="wrap"]/td/div/table/tbody/tr[1]/td[1]/a')
    for element in links:
        property_links.append(element.get_attribute('href'))
    return property_links

# Defining function used for scraping more pages
def find_links2(i, property_links):
    url = 'https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/warszawa/?page=' + str(i)
    driver.get(url)
    time.sleep(5)
    property_links = list(set(find_links1(property_links)))
    time.sleep(5)
    return property_links

property_links = []
property_links = find_links1(property_links)

# If bool parameter is set to True we limit links to 100, which means we scrap from max 4 pages
i = 2
if limit:
    while i < 4:
        property_links = find_links2(i, property_links)
        i = i + 1
    property_links = property_links[:100]
else:
    while i < 25:
        property_links = find_links2(i, property_links)
        i = i + 1

print('Number of property offers: ', len(property_links))

###########################################################################
################## Scraping information on each property ##################
###########################################################################

# d = pd.DataFrame({'name':[], 'price':[], 'key_words':[], 'description':[], 'telephone':[], 'map':[]})
 
# for url in property_links:
#     driver.get(url)
url = property_links[0]

driver.get(url)
time.sleep(5)

regexp = re.compile(r'otodom')
if regexp.search(url):
    print('* otodom scraping is at work *')
    button = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
    button.click()

    name = driver.find_element(By.XPATH, '//h1').get_attribute("innerHTML").splitlines()[0]
    print(name)
else:
    print('* olx site scraping is at work *')
    name = driver.find_element(By.XPATH, '//h1').get_attribute("innerHTML").splitlines()[0]
    print(name)


    