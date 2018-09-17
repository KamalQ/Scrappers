import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

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
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chrome_options=options, executable_path=chromedriver)
driver.get("https://coinmarketcal.com")

page_count = 1
list_entries = []

while True:
    page_count += 1

    for entry in driver.find_elements_by_class_name('card__body'):
        coin_name = entry.find_element_by_xpath('.//h5[@class="card__coins"]/a').text
        date = entry.find_element_by_xpath('.//a/h5[@class="card__date"]').text
        event_name = entry.find_element_by_xpath('.//a/h5[@class="card__title"]').text
        list_entries.append({'name': coin_name, 'date': date, 'event_name': event_name})

    try:
        element = driver.find_element_by_class_name("pagination")
        driver.execute_script("arguments[0].scrollIntoView();", element)
        driver.find_element_by_link_text(str(page_count)).click()
    except NoSuchElementException:
        break
    except Exception as Ex:
        driver.find_element_by_link_text(str(page_count)).click()


df_entries = pd.DataFrame.from_dict(list_entries)
print(df_entries)
df_entries.to_csv('Coin_Market_Cal_Scrapped_Data.csv')

driver.quit()