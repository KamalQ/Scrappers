import pandas as pd
import numpy as np
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

    def fetch_symbol_name(self):
        read_dictionary = np.load('../CoinMarketCap/List_of_crypto_symbols.npy').item()
        symbol_name = read_dictionary[self]
        return symbol_name

    def close_sign_in_prompt(self):
        self.driver.find_element_by_css_selector('i.popupCloseIcon.largeBannerCloser').click()
        fetch_crypto_hist_data.get_to_page(self)

    def get_to_page(self):
        symbol_name = fetch_crypto_hist_data.fetch_symbol_name(self.symbol)
        symbol = self.symbol.lower()
        symbol_name = symbol_name.lower()
        self.driver.get('https://ca.investing.com/crypto/{}/{}-btc-historical-data'.format(symbol_name, symbol))
        start_date = '01/01/2016'
        try:
            self.driver.find_elements_by_class_name('datePickerIcon')[1].click()
            self.driver.find_element_by_id('startDate').clear()
            self.driver.find_element_by_id('startDate').send_keys(start_date)
            self.driver.find_element_by_id('applyBtn').click()
        except:
            fetch_crypto_hist_data.close_sign_in_prompt(self)

    def fetch_data(self,symbol):
        self.symbol = symbol
        fetch_crypto_hist_data.get_to_page(self)


if __name__ == '__main__':
    scrapper = fetch_crypto_hist_data()
    scrapper.fetch_data('TRX')