*University of Warsaw
WNE*

# APPLICATION OF FF3 AND CAPM MODELS ON POLISH STOCK MARKET

The final project for Reproducible Research course is prepared to replicate [the paper](https://www.researchgate.net/publication/265152344_Applying_Fama_and_French_Three_Factors_Model_and_Capital_Asset_Pricing_Model_in_the_Stock_Exchange_of_Vietnam) made by Tran Viet Hoang & Nguyen Anh Phong, which aims to assess the application of Fama and French three factors models in Vietnam's stock market. Due to lack of original data from Vietnam, we decided to apply original methodology for polish stock market to test if we will have the same conclusions. 

Prepared by:
* Alparslan Erol
* Oleksii Zymin
* Sergey Amarin 

## Theoretical basis
* **Capital Assest Pricing Model (CAPM)** which was introduced by Sharpe (1964), Lintner (1965)
* Considers the relationship between the expected return of an asset and its systematic risk, measured by beta (β)
* Efficient market hypothesis - views the price as a proxy for all the information available in the market
* The return difference among portfolios is attributed to various risk factors underlying different capital assets
* Higher risk comes with a higher return for most the stocks
* **Fama and French (FF)** in 1992 examined the market size and book-to-market ratio and concluded that those two factors could explain expected returns:
1)  Small minus Big - additional return from investing in stocks of companies with relatively small market capitalization
2) High minus Low - additional return from investing in stocks of companies with high book-to-market values

## System
Windows 10 Pro for Workstations
, Version	21H1
, OS build	19043.1706

Python 3.8.13 (default, Mar 28 2022, 06:59:08) [MSC v.1916 64 bit (AMD64)]


## Data scrapping

For web-scrapping we utilized following libraries:
```python
from bs4 import BeautifulSoup     #version 4.9.3
from selenium import webdriver    #version 3.14.1
import requests                   #verion 2.27.1
```
We used publicly available data in the Web. Values from companies' financial statements were scrapped from [Bankier.pl](https://www.bankier.pl/), while stock market data was scrapped from [Stooq.pl](http://stooq.pl/).

Variables:
 1. Stock name
 2. Period 
 3. Close stock prices
 4. Stocks returns
 5. WIG index price
 6. WIG returns
 7. Number of shares
 8. Total assets
 8. Market value


## Usage


```python

```

## Results
