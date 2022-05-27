import pandas as pd
import itertools
import time
from ..utils.utils import (
    get_chrome_driver,
    dates_format,
    setup_selenium_env,
)

# setup chrome driver
driver = get_chrome_driver()

###YOU HAVE 20 SEC ENTER CAPTCHA AND CHOOSE QUARTERLY DATA BULLET AND PRESS SHOW BUTTON###
setup_selenium_env(driver, "wig")

text = driver.find_element_by_xpath('//*[@id="fth1"]').text
text_df = text.split()[8:]

list_to_df = []
for page_num in range(1, 5):
    url = "https://stooq.com/q/d/?s=wig&i=q&l=" + str(page_num)
    driver.get(url)
    text = driver.find_element_by_xpath('//*[@id="fth1"]').text
    text_df = text.split()[8:]
    n = 11
    list_to_add = [text_df[i : i + n] for i in range(0, len(text_df), n)]
    list_to_df.append(list_to_add)
    flat_list = itertools.chain(*list_to_df)
    flat_list = list(flat_list)

wig_df = pd.DataFrame(
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
# dates formatting
wig_df = dates_format(wig_df)
# save to csv
wig_df.to_csv("./data_scraper/output/wig_df.csv", index=False)
