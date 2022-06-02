import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller


def get_wig_list() -> pd.DataFrame:
    """
    This is a function that we have created and use it as utility function which is getting wig_data in a list.
    :return: Returns wig_data in a list.
    """
    url = "https://www.bankier.pl/inwestowanie/profile/quote.html?symbol=WIG"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    wig = soup.find("table", {"class": "sortTableMixedData"})
    wig_list = pd.read_html(str(wig))[0]
    wig_list.loc[wig_list.Ticker == "OAT", "Ticker"] = "MOC"
    return wig_list


def get_chrome_driver() -> webdriver.Chrome:
    """
    This is a function that we have created and use it as utility function which is creating selenium chrome webdriver
    for our both wig and company data scraper pipeline.
    :return: Returns the Chrome web driver based on the arguments below.
    """
    chromedriver_autoinstaller.install()
    # Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors-spki-list")
    chrome_options.add_argument("--ignore-certificate-errors")

    return webdriver.Chrome(options=chrome_options)
