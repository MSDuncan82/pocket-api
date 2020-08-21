import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def start_browser_auth(url="https://www.google.com", sleep=60):
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=chrome-data")
    chromedriver_path = "/usr/local/bin/chromedriver"
    broswer = webdriver.Chrome(chromedriver_path, options=chrome_options)
    chrome_options.add_argument("user-data-dir=chrome-data")
    broswer.get(url)
    time.sleep(sleep)  # Time to enter credentials
    broswer.quit()


if __name__ == "__main__":
    url = "https://www.medium.com"
    start_browser_auth(url)
