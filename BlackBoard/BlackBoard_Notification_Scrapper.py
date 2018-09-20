import pandas as pd
import re
import datetime as dt, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class fetch_BlackBoard:

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

    def login(self):
        with open('./BlackBoard_pass.txt') as credentials_file:
            credentials = credentials_file.readlines()
        username = credentials[0]
        password = credentials[1]
        username = re.findall('"([^"]*)"', username)
        password = re.findall('"([^"]*)"', password)
        self.driver.get('https://uoit.blackboard.com/')
        self.driver.find_element_by_id('username').send_keys(username)
        self.driver.find_element_by_id('password').send_keys(password)
        self.driver.find_element_by_class_name('btn-submit').click()

    def notifications(self):
        fetch_BlackBoard.login(self)
        self.driver.find_element_by_id('global-nav-link').click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'AlertsOnMyBb_____AlertsTool')))
        self.driver.find_element_by_id('AlertsOnMyBb_____AlertsTool').click()
        self.driver.quit()


if __name__ == '__main__':
    scrapper = fetch_BlackBoard()
    scrapper.notifications()
