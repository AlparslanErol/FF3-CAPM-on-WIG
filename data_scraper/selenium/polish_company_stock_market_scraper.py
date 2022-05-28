import pandas as pd
import time
import itertools
import time
from ..utils.utils import (
    get_wig_list,
    get_chrome_driver,
    dates_format,
    setup_selenium_env,
)

# setup chrome driver
driver = get_chrome_driver()
# getting the list of tickers
wig_list = get_wig_list()

###YOU HAVE 20 SEC ENTER CAPTCHA AND CHOOSE QUARTERLY DATA BULLET AND PRESS SHOW BUTTON###
setup_selenium_env(driver, "company")

# for each company from wig_list we scrap stock market data and append to final data frame
wig_stocks = pd.DataFrame()
for ticker in wig_list.Ticker:
    list_to_df = []
    try:
        for page_num in range(1, 5):
            url = "https://stooq.com/q/d/?s=" + str(ticker) + "&i=q&l=" + str(page_num)
            driver.get(url)
            text = driver.find_element_by_xpath('//*[@id="fth1"]').text
            text_df = text.split()[8:]
            # the next logic excludes from scrapping dividends, splitting and other unnecessary for our project events.
            for item in text_df:
                if item in ["Split", "Dividend", "Other"] and text_df[
                    text_df.index(item) + 2
                ] in ["Preemptive", "Prepurchase", "Preaccession"]:
                    del text_df[text_df.index(item) - 3 : text_df.index(item) + 6]
                else:
                    if item in [
                        "Preemptive",
                        "Prepurchase",
                        "Preaccession",
                    ] and text_df[text_df.index(item) + 3] in [
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
                            del text_df[
                                text_df.index(item) - 3 : text_df.index(item) + 6
                            ]
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
                                        text_df.index(item)
                                        - 3 : text_df.index(item)
                                        + 3
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

            n = 11
            list_to_add = [text_df[i : i + n] for i in range(0, len(text_df), n)]
            list_to_df.append(list_to_add)

    except:
        try:
            if driver.find_element_by_xpath('//*[@id="l"]/a').text == "Change code":
                time.sleep(30)
                text = driver.find_element_by_xpath('//*[@id="fth1"]').text
                text_df = text.split()[8:]
                for item in text_df:
                    if item in ["Split", "Dividend", "Other"] and text_df[
                        text_df.index(item) + 2
                    ] in ["Preemptive", "Prepurchase", "Preaccession"]:
                        del text_df[text_df.index(item) - 3 : text_df.index(item) + 6]
                    else:
                        if item in [
                            "Preemptive",
                            "Prepurchase",
                            "Preaccession",
                        ] and text_df[text_df.index(item) + 3] in [
                            "Preemptive",
                            "Prepurchase",
                            "Preaccession",
                        ]:
                            del text_df[
                                text_df.index(item) - 3 : text_df.index(item) + 7
                            ]
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
                                del text_df[
                                    text_df.index(item) - 3 : text_df.index(item) + 6
                                ]
                            else:
                                if item in ["Split", "Dividend", "Other"] and text_df[
                                    text_df.index(item) + 2
                                ] in ["Split", "Dividend", "Other"]:
                                    del text_df[
                                        text_df.index(item)
                                        - 3 : text_df.index(item)
                                        + 5
                                    ]
                                else:
                                    if item in ["Split", "Dividend", "Other"]:
                                        del text_df[
                                            text_df.index(item)
                                            - 3 : text_df.index(item)
                                            + 3
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
                n = 11  # number of variables
                list_to_add = [text_df[i : i + n] for i in range(0, len(text_df), n)]
                list_to_df.append(list_to_add)

            else:
                pass

        except:
            pass

    # data pre-formatting
    flat_list = itertools.chain(*list_to_df)
    flat_list = list(flat_list)

    stock_df = pd.DataFrame(
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
    stock_df["Ticker"] = ticker
    stock_df.loc[stock_df.No == "1", "vol"] = stock_df.loc[
        stock_df.No == "1", "perc_change"
    ]
    stock_df.loc[stock_df.No == "1", "perc_change"] = None

    wig_stocks = wig_stocks.append(stock_df)

wig_stocks = dates_format(wig_stocks)

# save to csv
wig_stocks.to_csv("./data_scraper/output/wig_stocks.csv", index=False)
