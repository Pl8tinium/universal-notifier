from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import os

class Webscraper:
    def __init__(self, chromedriver_path='', auto_cookie_ext_url=''):
        options = Options()
        options.add_argument('--disable-gpu')
        if (auto_cookie_ext_url != ''): 
            path_for_ext_file = './tmpfiles'
            if not os.path.exists(path_for_ext_file):
                os.mkdir(path_for_ext_file)
            if not os.path.isfile('./tmpfiles/ext.crx'):
                r = requests.get(url=auto_cookie_ext_url)
                open('./tmpfiles/ext.crx', "wb").write(r.content)
            options.add_extension('./tmpfiles/ext.crx')
        else:
            # unfortunately cant use extensions in chrome headless mode
            # should apparently work in firefox
            # https://stackoverflow.com/questions/62344970/unknown-error-failed-to-wait-for-extension-background-page-to-load-chrome-exte#:~:text=Chrome%20does%20not%20support%20headless%2C%20but%20apparently%20Firefox%20does.%20Some%20relevant%20discussions%3A
            options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging']) #ignore useless err msg
        if chromedriver_path == '':
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        else:
            self.driver = webdriver.Chrome(executable_path=chromedriver_path, options=options) #local chromedriver preinstalled
    def __access_site(self, url):
        self.driver.get(url)
        time.sleep(10)

    def __execute_js(self, script):
        return self.driver.execute_script(script)

    def check_site(self, url, script):
        self.__access_site(url)
        result = self.__execute_js(script)
        self.driver.close()
        return result


