from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen
import time
import json
import sys

sys.path.append(".")
CHROME_DATA_PATH = "/home/mike/projects/pocket/pocket-api/chrome-data"


def print_pdf(browser, url):

    browser.get(url)
    browser.execute_script(
        """window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })"""
    )
    time.sleep(1)
    browser.execute_script("window.print();")
    time.sleep(1)


def print_pdfs(url_list):

    chrome_options = Options()
    settings = {
        "recentDestinations": [
            {"id": "Save as PDF", "origin": "local", "account": "",}
        ],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
    }
    prefs = {"printing.print_preview_sticky_settings.appState": json.dumps(settings)}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--kiosk-printing")
    chrome_options.add_argument(f"--user-data-dir={CHROME_DATA_PATH}")
    chromedriver_path = "/usr/local/bin/chromedriver"
    browser = webdriver.Chrome(
        chrome_options=chrome_options, executable_path=chromedriver_path
    )
    chrome_options.add_argument(f"--user-data-dir={CHROME_DATA_PATH}")

    for url in url_list:
        print_pdf(browser, url)

    browser.quit()


if __name__ == "__main__":

    url_list = ["https://towardsdatascience.com/data-classes-in-python-8d1a09c1294b"]

    print_pdfs(url_list)
