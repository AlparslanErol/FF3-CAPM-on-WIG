*University of Warsaw WNE*

# Application of FF3 and CAPM Models on Polish Stock Market

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

## System and Reproducibility
Windows 10 Pro for Workstations
, Version	21H1
, OS build	19043.1706

Python 3.6.13 :: Anaconda, Inc.

To create and reproduce the same result that we had, please use ``environment.yml`` file to create exactly the same
conda environment as we have.

1. Create the environment from the ``environment.yml`` file:

```shell
conda env create -f environment.yml -n ff3_env
```

The first line of the ``yml`` file sets the new environment's name. For details see Creating an environment file manually.

2. Activate the new environment: ``conda activate myenv``

3. Verify that the new environment was installed correctly:
```shell
conda env list
```
You can also use ``conda info --envs``.


## Data scrapping

For web-scrapping we utilized following libraries:
```python
from bs4 import BeautifulSoup     #version 4.9.3
from selenium import webdriver    #version 3.14.1
import requests                   #verion 2.27.1
```
We used publicly available data in the Web. Values from companies' financial statements were scrapped
from [Bankier.pl](https://www.bankier.pl/), while stock market data was scrapped from [Stooq.pl](http://stooq.pl/).

Selenium part of the code has been written with OOP coding principles.

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

> You can find more detailed explanation into the code comments.

### BS4 Scraper
Beautiful soup has been used to scrape wig_data from ``bankier.pl`` to create ``wig_data.csv`` under the following
path ``/data_scraper/output/``.

To run bs4 scraper please use the following command:
```shell
python -m data_scraper.bs4.bs4_scraper
```

### Selenium Scraper
Selenium scraper triggered by an argument from the terminal to decide the type of scraper if it will be 
a ``company`` type scraper or a ``wig`` type scraper. Based on the type of scrape, the selenium data scraper pipeline 
changes and gather ``wig_stocks.csv`` data from ``company`` type scraper and ``wig_df.csv`` data from 
``wig`` type scraper into the path ``/data_scraper/output/``.

To run selenium scraper for both ``company`` and ``wig`` type scraper please use the following command:
```shell
# For company type scraper
python -m data_scraper.selenium.main -s company

# For company type scraper
python -m data_scraper.selenium.main -s wig
python -m data_scraper.selenium.main # wig is default
```

### Generate Final Data
To generate the final data into the path ``/data_scraper/output/final_data`` based on the data
scraped from ``bs4`` and ``selenium`` types, please use the following command:
```shell
# For final data
python -m data_scraper.main
```
This command will create 3 different csv files for usage:
1. ``final_df_long.csv``
2. ``final_df_short_ret.csv``
3. ``final_df_short_ret_clean.csv``

## Tests
Under ``tests`` folder, please find our test pipeline by performing unit testing on the functions and methods
that we have written into the scraping part of the code.

Please use the following command after you create the conda environment with all dependencies 
```shell
pytest tests/ --verbose
```

You can also run each unittests separately.

## Results
Please find our final part of the project as an exploration into the ``.ipynb`` file under ``capm_ff3_models`` folder
for Reproducible Research course is prepared to replicate 
[the paper](https://www.researchgate.\net/publication/265152344_Applying_Fama_and_French_Three_Factors_Model_and_Capital_Asset_Pricing_Model_in_the_Stock_Exchange_of_Vietnam) 
made by Tran Viet Hoang & Nguyen Anh Phong, which aims to assess the application of Fama and French three factors models
in Vietnam's stock market. Due to lack of original data from Vietnam, we decided to apply original methodology for
polish stock market to test if we will have the same conclusions.

Even though due to different data sets used for the original research and our project we couldn't fully numerically
recreate the original findings, however, we obtained quite similar results from conceptual and statistical point of view.
For both our results and original estimates FF3 model outperformed CAPM in terms of adjusted R-squared results for
most of the portfolios of stocks. Also, for both our results and original research FF3 produced the worst results for
B/M portfolio with some factors being statistically insignificant and thus irrelevant for explanation of variation of
portfolio stock returns.