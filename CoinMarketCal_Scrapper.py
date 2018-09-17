import pandas as pd
import datetime as dt, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


class fetch_coinMarketCal:

    def __init__(self):
        pd.set_option('max_rows', 100)
        pd.set_option('max_columns', 10)
        self.options = Options()
        # options.add_argument("--headless")
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('start-maximized')
        self.options.add_argument('disable-infobars')
        self.options.add_argument("--disable-extensions")
        self.chromedriver = "/usr/local/bin/chromedriver"
        self.driver = webdriver.Chrome(chrome_options=self.options, executable_path=self.chromedriver)


    # past events == https://coinmarketcal.com/pastevents
    def upcoming_events(self):
        self.driver.get("https://coinmarketcal.com")
        page_count = 1
        list_entries = []
        time_stamp = dt.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

        while True:
            for entry in self.driver.find_elements_by_class_name('card__body'):
                coin_name = entry.find_element_by_xpath('.//h5[@class="card__coins"]/a').text
                date = entry.find_element_by_xpath('.//a/h5[@class="card__date"]').text
                event_name = entry.find_element_by_xpath('.//a/h5[@class="card__title"]').text
                additional_info = entry.find_element_by_xpath('.//div/p[@class="card__description"]').text
                #link = entry.find_element_by_xpath('.//h5[@class="card__coins"]/a').text
                symbol = coin_name.split('(', 1)[1].split(')')[0]
                list_entries.append({'symbol': symbol, 'name': coin_name, 'date': date, 'event_name': event_name, 'additional_info': additional_info})
            try:
                print(time_stamp, 'Finished scraping data from page #', (page_count))
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
        df_entries.to_csv('CoinMarketCal_Upcoming_Scrapped_Data.csv')
        #Todo add column for hyperlink, sort by symbol in df
        self.driver.quit()


if __name__ == '__main__':
    scrapper = fetch_coinMarketCal()
    scrapper.upcoming_events()