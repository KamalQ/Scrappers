import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# This code fetches a complete list off all coins listed on https://coinmarketcap.com/coins/views/all/
# Saves a Dictionary with Symbol and Symbol name

class fetch_crypto_list:

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

    def fetch_list(self):
        self.driver.get('https://coinmarketcap.com/coins/views/all/')
        list_symbol = []
        list_symbol_name = []
        rows = self.driver.find_elements(By.TAG_NAME, "tr")
        rows.pop(0)
        for row in rows:
            symbol = row.find_element_by_css_selector('td.text-left.col-symbol').text
            symbol_name = row.find_element_by_css_selector('a.currency-name-container.link-secondary').text
            print(symbol_name, symbol)
            list_symbol.append(symbol)
            list_symbol_name.append(symbol_name)

        dict_symbol_and_name = dict(zip(list_symbol,list_symbol_name))
        np.save('../CoinMarketCap/List_of_crypto_symbols.npy', dict_symbol_and_name)
        read_dictionary = np.load('../CoinMarketCap/List_of_crypto_symbols.npy').item()
        print(read_dictionary['TRX'])
        # self.driver.quit()


if __name__ == '__main__':
    scrapper = fetch_crypto_list()
    scrapper.fetch_list()