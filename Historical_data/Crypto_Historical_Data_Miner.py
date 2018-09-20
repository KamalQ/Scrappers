import pandas as pd
import datetime as dt, time
import pymongo
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


class fetch_crypto_hist_data:

    def __init__(self):
        pd.set_option('max_rows', 100)
        pd.set_option('max_columns', 10)
        self.options = Options()
        # self.options.add_argument("--headless")
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('start-maximized')
        self.options.add_argument('disable-infobars')
        self.options.add_argument("--disable-extensions")
        self.chromedriver = "/usr/local/bin/chromedriver"
        self.driver = webdriver.Chrome(chrome_options=self.options, executable_path=self.chromedriver)

    def fetch_symbol_name(self,symbol):
        name = symbol
        return name

    def schedule(self, symbol):
        symbol_name = fetch_crypto_hist_data.fetch_symbol_name(self,symbol)
        self.driver.get('https://ca.investing.com/crypto/{}/{}-btc-historical-data'.format(symbol_name,symbol))
        # self.driver.find_elements_by_id('p_chan_links_lnk')[10].click()
        # self.driver.find_element_by_partial_link_text('Look-up Classes to Add').click()
        # self.driver.quit()


if __name__ == '__main__':
    scrapper = fetch_crypto_hist_data()
    scrapper.schedule('xrp')