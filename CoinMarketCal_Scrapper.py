import pandas as pd
import datetime as dt, time
import pymongo
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

#Todo try to fetch event type, date event was added/posted, votes and percent- for event type i should create my own cross refence from list and match,
# sort from master list of event types based on all collected data input/names
#Date Data was collected Sept 17, 2018

class fetch_coinMarketCal:

    def __init__(self):
        pd.set_option('max_rows', 100)
        pd.set_option('max_columns', 10)
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('start-maximized')
        self.options.add_argument('disable-infobars')
        self.options.add_argument("--disable-extensions")
        self.chromedriver = "/usr/local/bin/chromedriver"
        self.driver = webdriver.Chrome(chrome_options=self.options, executable_path=self.chromedriver)
        self.client = pymongo.MongoClient('localhost', 27017)
        self.database = self.client['CoinMarketCal']

    def save_to_database(self, dataframe):
        time_stamp = dt.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        collection = self.database['CoinMarketCal_events']
        dataframe.reset_index(inplace=True)
        data_frame_json = json.loads(dataframe.T.to_json()).values()

        starttime = dt.datetime.now()
        print(time_stamp, 'Saving data to database...')
        for entry in data_frame_json:
            link = entry['link']
            collection.update({'link': link}, entry, upsert=True)

        endtime = dt.datetime.now()
        print(time_stamp, 'Total elapsed time:', endtime - starttime)
        return

    def events(self, event_link, file_name):
        self.driver.get(event_link)
        page_count = 1
        list_entries = []
        time_stamp = dt.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

        while True:
            for entry in self.driver.find_elements_by_class_name('card__body'):
                coin_name = entry.find_element_by_xpath('.//h5[@class="card__coins"]/a').text
                date = entry.find_element_by_xpath('.//a/h5[@class="card__date"]').text
                event_name = entry.find_element_by_xpath('.//a/h5[@class="card__title"]').text
                additional_info = entry.find_element_by_xpath('.//div/p[@class="card__description"]').text
                link = entry.find_elements_by_class_name('link-detail')[1].get_attribute('href')
                symbol = coin_name.split('(', 1)[1].split(')')[0]
                list_entries.append({'symbol': symbol, 'name': coin_name, 'date': date, 'event_name': event_name,
                                     'additional_info': additional_info, 'link': link})
            try:
                print(time_stamp, 'Finished scraping data from page #', page_count)
                element = self.driver.find_element_by_class_name("pagination")
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                page_count += 1
                self.driver.find_element_by_link_text(str(page_count)).click()
            except NoSuchElementException:
                break
            except Exception as Ex:
                print(time_stamp, '--- Error occurred : ', Ex)

        df_entries = pd.DataFrame.from_dict(list_entries)
        print(df_entries)
        fetch_coinMarketCal.save_to_database(self,df_entries)
        df_entries.to_csv(file_name)
        self.driver.quit()


if __name__ == '__main__':
    scrapper = fetch_coinMarketCal()
    scrapper.events('https://coinmarketcal.com', 'CoinMarketCal_Scrapped_Data.csv')
    scrapper.events('https://coinmarketcal.com/pastevents', 'CoinMarketCal_Past_Scrapped_Data.csv')