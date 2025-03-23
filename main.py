from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def main():
    ccb = CCBot()
    ccb.start()
    ccb.select_language()
    # TODO: Start timing here
    multiplier = 1
    while True:
        for i in range(int(10*multiplier)):
            ccb.click_cookie()
        ccb.buy_nth_upgrade(0)
        for i in range(6):
            ccb.buy_nth_product(5-i)
        multiplier *= 1.05
    # TODO: End timing here
    ccb.end()

class Timer:
    def __init__(self, time_seconds: int):
        self.duration = time_seconds

class CCBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.url = "https://orteil.dashnet.org/cookieclicker/"

        self.current_cps = 0

    def start(self):
        self.driver.get(self.url)

    def end(self):
        self.driver.quit()

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

    # Information

    def get_cps(self):
        element = self.driver.find_element(By.ID, "cookiesPerSecond")
        self.current_cps = element.get_attribute("value")
        print(self.current_cps)


    def get_total_cookies(self):
        pass

if __name__ == "__main__":
    main()