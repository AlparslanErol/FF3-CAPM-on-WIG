import typing
import pandas as pd
import time
import itertools
import time
from ..utils.utils import (
    get_wig_list,
    get_chrome_driver,
)


class SeleniumScraper:
    def __init__(self) -> None:
        # setup chrome driver
        self.driver = get_chrome_driver()
        # getting the list of tickers
        self.wig_list = get_wig_list()
        # for each company from wig_list we scrap stock market data and append to final data frame
        self.wig_stocks = pd.DataFrame()

    def _setup_selenium_env(self, type: str):
        url = (
            "https://stooq.com/q/d/?s=BMC&i=q&l=1"
            if type == "company"
            else "https://stooq.com/q/d/?s=wig&c=0&i=q"
        )
        self.driver.get(url)
        self.driver.find_element_by_xpath(
            "/html/body/div/div[2]/div[1]/div[2]/div[2]/button[1]"
        ).click()  # cookies
        time.sleep(20)

    def company_stock_scraper(self):
        # YOU HAVE 20 SEC ENTER CAPTCHA AND CHOOSE QUARTERLY DATA BULLET AND PRESS SHOW BUTTON
        self._setup_selenium_env("company")
        for ticker in self.wig_list.Ticker:
            list_to_df = []
            try:
                for page_num in range(1, 5):
                    self._get_url_driver(ticker, page_num)
                    text_df = self._prepare_text_df()
                    text_df = self._exclude_from_scraping(text_df)
                    self._list_to_add(text_df, list_to_df)
            except:
                try:
                    if (
                        self.driver.find_element_by_xpath('//*[@id="l"]/a').text
                        == "Change code"
                    ):
                        time.sleep(30)
                        text_df = self._prepare_text_df()
                        text_df = self._exclude_from_scraping(text_df)
                        self._list_to_add(text_df, list_to_df)
                    else:
                        pass
                except:
                    pass
            self._data_pre_formatting(list_to_df, ticker)
        self.wig_stocks = self.dates_format(self.wig_stocks)
        # save to csv
        self.wig_stocks.to_csv("./data_scraper/output/wig_stocks.csv", index=False)

    def wig_market_data_scraper(self):
        # YOU HAVE 20 SEC ENTER CAPTCHA AND CHOOSE QUARTERLY DATA BULLET AND PRESS SHOW BUTTON
        self._setup_selenium_env("wig")
        list_to_df = []
        for page_num in range(1, 5):
            self._get_url_driver("", page_num)
            text_df = self._prepare_text_df()
            self._list_to_add(text_df, list_to_df)
        self._data_pre_formatting(list_to_df, ticker="")
        self.wig_stocks = self.dates_format(self.wig_stocks)
        # save to csv
        self.wig_stocks.to_csv("./data_scraper/output/wig_df.csv", index=False)

    def _get_url_driver(self, ticker: str, page_num: int):
        url = (
            "https://stooq.com/q/d/?s=wig&i=q&l=" + str(page_num)
            if ticker == ""
            else "https://stooq.com/q/d/?s=" + str(ticker) + "&i=q&l=" + str(page_num)
        )
        self.driver.get(url)

    def _prepare_text_df(self) -> typing.List:
        text = self.driver.find_element_by_xpath('//*[@id="fth1"]').text
        text_df = text.split()[8:]
        return text_df

    @staticmethod
    def _exclude_from_scraping(text_df: typing.List) -> typing.List:
        # the next logic excludes from scrapping dividends, splitting and other unnecessary for our project events.
        for item in text_df:
            if item in ["Split", "Dividend", "Other"] and text_df[
                text_df.index(item) + 2
            ] in ["Preemptive", "Prepurchase", "Preaccession"]:
                del text_df[text_df.index(item) - 3 : text_df.index(item) + 6]
            else:
                if item in ["Preemptive", "Prepurchase", "Preaccession",] and text_df[
                    text_df.index(item) + 3
                ] in [
                    "Preemptive",
                    "Prepurchase",
                    "Preaccession",
                ]:
                    del text_df[text_df.index(item) - 3 : text_df.index(item) + 7]
                else:
                    if item in [
                        "Preemptive",
                        "Prepurchase",
                        "Preaccession",
                    ] and text_df[text_df.index(item) + 3] in [
                        "Split",
                        "Dividend",
                        "Other",
                    ]:
                        del text_df[text_df.index(item) - 3 : text_df.index(item) + 6]
                    else:
                        if item in ["Split", "Dividend", "Other"] and text_df[
                            text_df.index(item) + 2
                        ] in ["Split", "Dividend", "Other"]:
                            del text_df[
                                text_df.index(item) - 3 : text_df.index(item) + 5
                            ]
                        else:
                            if item in ["Split", "Dividend", "Other"]:
                                del text_df[
                                    text_df.index(item) - 3 : text_df.index(item) + 3
                                ]
                            else:
                                if item in [
                                    "Preemptive",
                                    "Prepurchase",
                                    "Preaccession",
                                ]:
                                    del text_df[
                                        text_df.index(item)
                                        - 3 : text_df.index(item)
                                        + 4
                                    ]
        return text_df

    @staticmethod
    def _list_to_add(text_df: typing.List, list_to_df: typing.List):
        n = 11
        list_to_add = [text_df[i : i + n] for i in range(0, len(text_df), n)]
        list_to_df.append(list_to_add)

    def _data_pre_formatting(self, list_to_df: typing.List, ticker: str):
        # data pre-formatting
        flat_list = itertools.chain(*list_to_df)
        flat_list = list(flat_list)
        scraper_df = pd.DataFrame(
            flat_list,
            columns=[
                "No",
                "day",
                "mon",
                "year",
                "open",
                "high",
                "low",
                "close",
                "perc_change",
                "abs_change",
                "vol",
            ],
        )
        if ticker != "":
            scraper_df["Ticker"] = ticker
            scraper_df.loc[scraper_df.No == "1", "vol"] = scraper_df.loc[
                scraper_df.No == "1", "perc_change"
            ]
            scraper_df.loc[scraper_df.No == "1", "perc_change"] = None
        self.wig_stocks = self.wig_stocks.append(scraper_df)

    @staticmethod
    def dates_format(df: pd.DataFrame) -> pd.DataFrame:
        # dates reformatting
        df.loc[df.mon == "Dec", "mon"] = "12"
        df.loc[df.mon == "Mar", "mon"] = "03"
        df.loc[df.mon == "Jun", "mon"] = "06"
        df.loc[df.mon == "Sep", "mon"] = "09"
        df["period"] = df["day"] + "-" + df["mon"] + "-" + df["year"]
        df.drop(["day", "mon", "year"], axis=1, inplace=True)
        return df
