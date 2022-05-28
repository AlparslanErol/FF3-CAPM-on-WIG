# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
from ..utils.utils import get_wig_list

wig_list = get_wig_list()

# financial data
wig_data = pd.DataFrame()
wig_names = wig_list.Nazwa

counter = 1
for name in wig_names:
    page = 1
    fin_report = []
    while fin_report is not None:
        url = (
            "https://www.bankier.pl/gielda/notowania/akcje/"
            + str(name)
            + "/wyniki-finansowe/jednostkowy/kwartalny/standardowy/"
            + str(page)
        )
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        try:
            fin_report = soup.find("table")
            df2 = pd.read_html(str(fin_report))[0]
            df2 = df2.transpose().reset_index()
            df2.columns = df2.iloc[0, :]
            df2 = df2.drop(0)
            df2["symbol"] = name
            df2.set_index("symbol", inplace=True)

            wig_data = wig_data.append(df2)
            page += 1
        except:
            pass
    print(counter, name, len(wig_data))
    counter += 1

# data cleaning and formatting
for row in range(len(wig_data)):
    wig_data.iloc[row, 0] = wig_data["Unnamed: 0"][row].replace("IV Q ", "31-12-")
    wig_data.iloc[row, 0] = wig_data["Unnamed: 0"][row].replace("III Q ", "30-09-")
    wig_data.iloc[row, 0] = wig_data["Unnamed: 0"][row].replace("II Q ", "30-06-")
    wig_data.iloc[row, 0] = wig_data["Unnamed: 0"][row].replace("I Q ", "31-03-")
    for col in range(2, len(wig_data.columns)):
        try:
            wig_data.iloc[row, col] = int(
                re.sub(r"(\d)\s+(\d)", r"\1\2", wig_data.iloc[row, col])
            )
        except:
            pass

colnames = [
    "Date",
    "Currency",
    "Net sales revenues",
    "Profit (loss) on operating activities",
    "Gross profit (loss)",
    "Net profit (loss) parent",
    "Depreciation",
    "EBITDA",
    "Assets",
    "Equity",
    "Number of shares",
    "Earnings per share (zl)",
    "Book value per share (zl)",
]

banks = [
    "ALIOR",
    "BNPPPL",
    "BOS",
    "GETIN",
    "GETINOBLE",
    "HANDLOWY",
    "INGBSK",
    "MBANK",
    "MILLENNIUM",
    "PEKAO",
    "PKOBP",
    "SANPL",
    "SANTANDER",
    "UNICREDIT",
    "PZU",
]

# delete banks' info
wig_data_no_banks = wig_data.loc[
    [tickname for tickname in np.unique(wig_data.index.values) if tickname not in banks]
]
wig_data_no_banks = wig_data_no_banks.iloc[:, 0:13]
wig_data_no_banks.columns = colnames

# delete Q0000 and .1 data
wig_data_no_banks = wig_data_no_banks.reset_index()
wig_data_no_banks.loc[
    wig_data_no_banks["Date"].str.contains("(?i)0000", na=False)
    | wig_data_no_banks["Date"].str.contains("\\.", na=False),
].index
wig_data_clean = wig_data_no_banks.drop(
    wig_data_no_banks.loc[
        wig_data_no_banks["Date"].str.contains("(?i)Q", na=False)
        | wig_data_no_banks["Date"].str.contains("\\.", na=False),
    ].index
)
wig_data_clean.reset_index(drop=True, inplace=True)

# save to csv
wig_data_clean.to_csv("./data_scraper/output/wig_data.csv", index=False)
