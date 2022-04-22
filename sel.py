from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re

# Setting up a boolean parameter limiting the number of pages.
# NEED TO WORK ON BOOLEAN PARAMETER
limit = True

# Setting up and conneting to site using selenium tools

gecko_path = 'C:/Users/weron/anaconda3/Library/geckodriver'
options = webdriver.firefox.options.Options()
options.headless = False
driver = webdriver.Firefox(options = options, executable_path = gecko_path)

url = 'https://www.olx.pl/nieruchomosci/mieszkania/warszawa/'

driver.get(url)

time.sleep(5)

# Clicking cookies consent

button = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
button.click()

time.sleep(5)

# The site is displaying property offers in a table
# Getting links to properties by tr of class=wrap
property_links = []
links = driver.find_elements(By.XPATH, '//tr[@class="wrap"]/td/div/table/tbody/tr[1]/td[1]/a')
for element in links:
    property_links.append(element.get_attribute('href'))

# If bool parameter is set to True we limit links to 100
# NEED TO WORK ON BOOLEAN PARAMETER
i = 2
while len(property_links) <= 100:
    url = 'https://www.olx.pl/nieruchomosci/mieszkania/warszawa/?page=' + str(i)
    driver.get(url)
    time.sleep(5)
    links = driver.find_elements(By.XPATH, '//tr[@class="wrap"]/td/div/table/tbody/tr[1]/td[1]/a')
    for element in links:
        property_links.append(element.get_attribute('href'))
    property_links = list(set(property_links))
    time.sleep(2)
    i = i + 1

property_links = property_links[:100]

# for url in property_links:
#     driver.get(url)
url = property_links[0]
d = pd.DataFrame({'name':[], 'price':[], 'key_words':[], 'description':[], 'telephone':[], 'map':[]})
driver.get(url)
time.sleep(5)

regexp = re.compile(r'otodom')
if regexp.search(url):
    print('otodom scraping is at work')
    button = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
    button.click()
else:
    print('olx site is at work, but here is name of the property offer')
    name = driver.find_element(By.XPATH, '//h1').get_attribute("innerHTML").splitlines()[0]
    print(name)
    