import pandas as pd
import datetime, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

#todo figure out how to inital a class in python and add this into the init
pd.set_option('max_rows', 100)
pd.set_option('max_columns', 10)
options = Options()
# options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
chromedriver = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(chrome_options=options, executable_path=chromedriver)

class fetch_coinMarketCal():

    def upcoming_event(self):
        driver.get("https://coinmarketcal.com")
        page_count = 1
        list_entries = []
        time_stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

        while True:
            page_count += 1
            for entry in driver.find_elements_by_class_name('card__body'):
                coin_name = entry.find_element_by_xpath('.//h5[@class="card__coins"]/a').text
                date = entry.find_element_by_xpath('.//a/h5[@class="card__date"]').text
                event_name = entry.find_element_by_xpath('.//a/h5[@class="card__title"]').text
                additional_info = entry.find_element_by_xpath('.//div/p[@class="card__description"]').text
                list_entries.append({'name': coin_name, 'date': date, 'event_name': event_name, 'additional_info': additional_info})
            try:
                print(time_stamp, 'Finished scraping data from page #', (page_count-1))
                element = driver.find_element_by_class_name("pagination")
                driver.execute_script("arguments[0].scrollIntoView();", element)
                driver.find_element_by_link_text(str(page_count)).click()
            except NoSuchElementException:
                break
            except Exception as Ex:
                print(time_stamp, '--- Error occurred : ', Ex)

        df_entries = pd.DataFrame.from_dict(list_entries)
        print(df_entries)
        df_entries.to_csv('CoinMarketCal_Upcoming_Scrapped_Data.csv')
        driver.quit()


if __name__ == '__main__':
    init_scraper = fetch_coinMarketCal
    fetch_coinMarketCal.upcoming_event(init_scraper)