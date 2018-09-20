import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Opens Chrome and takes you to MyCampus portal(logs in for you)

class fetch_BlackBoard:

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

    def login(self):
        with open('./MyCampus/MyCampus_pass.txt') as credentials_file:
            credentials = credentials_file.readlines()
        username = credentials[0]
        password = credentials[1]
        username = re.findall('"([^"]*)"', username)
        password = re.findall('"([^"]*)"', password)
        self.driver.get('https://uoit.ca/mycampus/')
        self.driver.find_element_by_id('user').send_keys(username)
        self.driver.find_element_by_id('pass').send_keys(password)
        self.driver.find_element_by_css_selector(".button.small.float-right").click()

    def schedule(self):
        fetch_BlackBoard.login(self)
        self.driver.find_elements_by_id('p_chan_links_lnk')[10].click()
        # self.driver.find_element_by_partial_link_text('Look-up Classes to Add').click()
        # self.driver.quit()


if __name__ == '__main__':
    scrapper = fetch_BlackBoard()
    scrapper.schedule()