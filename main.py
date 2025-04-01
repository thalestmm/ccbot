# Core functionalities
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# Administrative tasks
import logging
import time
import yaml
import os

logging.basicConfig(level=logging.INFO)

def main():
    with open('config.yaml', 'r') as stream:
        data = yaml.safe_load(stream)

    DURATION_SECONDS = data['DURATION_SECONDS']
    BAKERY_NAME = data['BAKERY_NAME']

    ccb = CCBot()
    ccb.start()
    ccb.select_language()
    ccb.rename_shop(BAKERY_NAME)
    t = Timer(DURATION_SECONDS)
    multiplier = 1
    while True:
        for i in range(int(10*multiplier)):
            ccb.click_cookie()
            if time.time() >= t.end_time:
                break
        if time.time() >= t.end_time:
            break
        ccb.buy_nth_upgrade(0)
        for i in range(10):
            ccb.buy_nth_product(9-i)
        multiplier *= 1.05
    ccb.save_page_source()
    ccb.get_total_cookies()
    time.sleep(5)
    ccb.end(DURATION_SECONDS)

class Timer:
    def __init__(self, time_seconds: int):
        self.duration = time_seconds
        self.current_time = time.time()
        self.end_time = time.time() + time_seconds

class CCBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.url = "https://orteil.dashnet.org/cookieclicker/"

        self.total_cookies = None

    def start(self):
        self.driver.get(self.url)

    def end(self, duration_seconds: int):
        self.driver.quit()
        logging.info(f" Total cookies: {self.total_cookies}")
        logging.info(f" Run duration: {duration_seconds} seconds")
        try:
            os.remove("page_source.html")
        finally:
            logging.info(" Temp files removed")


    def select_language(self):
        time.sleep(5)
        element = self.driver.find_element(By.ID, "langSelect-EN")
        element.click()
        time.sleep(5)

    # Actions

    def click_cookie(self):
        element = self.driver.find_element(By.ID, "bigCookie")
        element.click()

    def buy_nth_product(self, n: int) -> None:
        try:
            element = self.driver.find_element(By.ID, f"product{n}")
            element.click()
        except:
            pass

    def buy_nth_upgrade(self, n: int) -> None:
        try:
            element = self.driver.find_element(By.ID, f"upgrade{n}")
            element.click()
        except:
            pass

    def rename_shop(self, bakery_name: str) -> None:
        element = self.driver.find_element(By.ID, "bakeryName")
        element.click()
        time.sleep(0.1)
        input_box = self.driver.find_element(By.ID, "bakeryNameInput")
        input_box.send_keys(f"{bakery_name}")
        input_box.send_keys(Keys.ENTER)
        logging.info(f" Bakery renamed to: {bakery_name}")
        time.sleep(0.1)

    # Information

    def save_page_source(self):
        element = self.driver.find_element(By.ID, "statsButton")
        element.click()
        source = self.driver.page_source
        with open ("page_source.html", "w", encoding="utf-8") as f:
            f.write(source)

    def get_total_cookies(self):
        soup = BeautifulSoup(open("page_source.html"), "html.parser")
        menu_div = soup.find("div", id="menu")
        listings = menu_div.find_all("div", class_="listing")
        self.total_cookies = listings[1].find("div", class_="price plain").text


if __name__ == "__main__":
    main()
