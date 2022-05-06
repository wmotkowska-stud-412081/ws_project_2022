import scrapy
import re

#creating list to which links to pages scraped will be appended
lista_linkow = []
#setting Boolean value to True = analysis is limited to 100 links
limit = True

#creating Link class in order to be able to append links to csv file later on
class Link(scrapy.Item):
    link = scrapy.Field()

#creating spider for offers scraping
class LinksSpider(scrapy.Spider):
    name = 'links'
    allowed_domains = ['https://olx.pl/']
    start_urls = ['https://olx.pl/d/nieruchomosci/mieszkania/sprzedaz/warszawa/']

#creating a list of links to pages with offers manually as we can't click through links as in selenium
#which results in enabling spider to scrape 4 links only (page 1,2,3 and last one = 25th)
    for i in range(2,26):
        start_urls.append('https://www.olx.pl/d/nieruchomosci/mieszkania/sprzedaz/warszawa/?page='+str(i))
#urls used for further offers scraping
    try:
        start_urls 
    except:
        start_urls = []

#main functionality of spider
    def parse(self, response):
        print(response)
        #select hyperlink (a) tags of class "css-1bbgabe.*" -> parts of offers urls
        xpath = '//a[re:test(@class, "css-1bbgabe.*")]//@href'
        selection = response.xpath(xpath)
        regexp = re.compile('.*otodom.*')
        for s in selection:
            #check if list of links does not exceed 100
            if limit: 
                #get the specific part of the link from selection and merge it with the default start
                l = Link()
                #check if the link is otodom or olx
                l['link'] ='https://olx.pl' + s.get()
                print('https://olx.pl' + s.get())
                if (regexp.search(l['link'])==None):
                    lista_linkow.append(l['link'])
                    #append to the list in order to keep an eye on length of the list
                if (regexp.search(l['link'])==None) and len(lista_linkow) <101:
                    #add the link to csv if it's olx offer
                    yield l
                    #append to the list in order to keep an eye on length of the list
                    
        

            

        
