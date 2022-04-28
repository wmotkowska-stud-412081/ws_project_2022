## WS project of group: 

### Karolina Kowalska
Working on Beautiful Soup.

### Magdalena Pruszyńska
Working on Scrapy. 
In order to get the information on flats offered, one needs to download both spiders from a scrapy project folder. The next step is going to command prompt, making sure that you are in a folder, where all of the spiders downloaded are and type:
# scrapy runspider spider_links.py -s USER_AGENT="custom_user" -o links.csv 
that should generate links.csv file in the same folder you and spiders are in.
The last step should be going back to your command prompt and typing:
# scrapy runspider spider2.py -s USER_AGENT="custom_user" -o final_data.csv
The final dataset should appear in your folder.

### Weronika Motkowska
Working on selenium.
To run the file one needs to change the gecko_path to path to geckodriver on own computer. Then in terminal write 'python sel.py'. Name 'selenium.py' brings confusion because of double-naming.

The links to property offers are conditioned on being from olx site as other team chose otodom for their project.
