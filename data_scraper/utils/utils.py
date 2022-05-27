import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from typing import List
from selenium import webdriver
import chromedriver_autoinstaller


def get_wig_list() -> List:
    url = "https://www.bankier.pl/inwestowanie/profile/quote.html?symbol=WIG"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    wig = soup.find("table", {"class": "sortTableMixedData"})
    wig_list = pd.read_html(str(wig))[0]
    wig_list.loc[wig_list.Ticker == "OAT", "Ticker"] = "MOC"
    return wig_list


def get_chrome_driver() -> webdriver.Chrome:
    chromedriver_autoinstaller.install()
    # Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(options=chrome_options)


# dates reformatting
def dates_format(df: pd.DataFrame) -> pd.DataFrame:
    df.loc[df.mon == "Dec", "mon"] = "12"
    df.loc[df.mon == "Mar", "mon"] = "03"
    df.loc[df.mon == "Jun", "mon"] = "06"
    df.loc[df.mon == "Sep", "mon"] = "09"
    df["period"] = df["day"] + "-" + df["mon"] + "-" + df["year"]
    df.drop(["day", "mon", "year"], axis=1, inplace=True)
    return df


def setup_selenium_env(driver, type):
    url = (
        "https://stooq.com/q/d/?s=BMC&i=q&l=1"
        if type == "company"
        else "https://stooq.com/q/d/?s=wig&c=0&i=q"
    )
    driver.get(url)
    driver.find_element_by_xpath(
        "/html/body/div/div[2]/div[1]/div[2]/div[2]/button[1]"
    ).click()  # cookies
    time.sleep(20)
