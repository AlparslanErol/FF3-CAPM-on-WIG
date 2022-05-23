import pandas as pd
import numpy as np
import time
from selenium import webdriver
import math
import requests 
from bs4 import BeautifulSoup 
import re
import string
import os
import yfinance as yf
#from yahoofinancials import YahooFinancials
from selenium import webdriver
import itertools
import time


#getting the list of tickers
url = 'https://www.bankier.pl/inwestowanie/profile/quote.html?symbol=WIG'
response=requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
wig = soup.find('table',{'class':"sortTableMixedData"})
wig_list = pd.read_html(str(wig))[0]
wig_list.loc[wig_list.Ticker == 'OAT', 'Ticker'] = 'MOC' #rename single ticker with its actual name

#polish companies market data scrapping

#setting up Selenium driver
driver = webdriver.Chrome(executable_path=r'D:\\UW\\2nd semester\\Webscrapping\\chromedriver.exe')
url = 'https://stooq.com/q/d/?s=BMC&i=q&l=1'

###YOU HAVE 20 SEC ENTER CAPTCHA AND CHOOSE QUARTERLY DATA BULLET AND PRESS SHOW BUTTON###
driver.get(url)
driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/div[2]/div[2]/button[1]').click()  #cookies
time.sleep(20)

#for each company from wig_list we scrap stock market data and append to final data frame
wig_stocks = pd.DataFrame()
for ticker in wig_list.Ticker:
    list_to_df = []
    try:
        for page_num in range(1,5):
            url = 'https://stooq.com/q/d/?s='+str(ticker)+'&i=q&l='+str(page_num)
            driver.get(url)
            text = driver.find_element_by_xpath('//*[@id="fth1"]').text
            text_df = text.split()[8:]   
    #the next logic excludes from scrapping dividends, splitting and other unnecessary for our project events.
            for item in text_df:
                if item in ['Split','Dividend', 'Other'] and text_df[text_df.index(item)+2] in ['Preemptive', 'Prepurchase', 'Preaccession']:
                    del text_df[text_df.index(item)-3:text_df.index(item)+6]
                else:
                    if item in ['Preemptive','Prepurchase','Preaccession'] and text_df[text_df.index(item)+3] in ['Preemptive','Prepurchase','Preaccession']:
                        del text_df[text_df.index(item)-3:text_df.index(item)+7]
                    else:
                        if item in ['Preemptive','Prepurchase','Preaccession'] and text_df[text_df.index(item)+3] in ['Split','Dividend', 'Other']:
                            del text_df[text_df.index(item)-3:text_df.index(item)+6]
                        else:
                            if item in ['Split','Dividend', 'Other'] and text_df[text_df.index(item)+2] in ['Split','Dividend', 'Other']:
                                del text_df[text_df.index(item)-3:text_df.index(item)+5]
                            else:
                                if item in ['Split','Dividend', 'Other']:
                                    del text_df[text_df.index(item)-3:text_df.index(item)+3]
                                else:
                                    if item in ['Preemptive', 'Prepurchase', 'Preaccession']:
                                        del text_df[text_df.index(item)-3:text_df.index(item)+4]
                                        
            n = 11 
            list_to_add = [text_df[i:i + n] for i in range(0, len(text_df), n)]
            list_to_df.append(list_to_add)
            
    except:
        try:
            if driver.find_element_by_xpath('//*[@id="l"]/a').text == 'Change code':
                time.sleep(30)
                text = driver.find_element_by_xpath('//*[@id="fth1"]').text
                text_df = text.split()[8:]   
                for item in text_df:
                    if item in ['Split','Dividend', 'Other'] and text_df[text_df.index(item)+2] in ['Preemptive', 'Prepurchase', 'Preaccession']:
                        del text_df[text_df.index(item)-3:text_df.index(item)+6]
                    else:
                        if item in ['Preemptive','Prepurchase','Preaccession'] and text_df[text_df.index(item)+3] in ['Preemptive','Prepurchase','Preaccession']:
                            del text_df[text_df.index(item)-3:text_df.index(item)+7]
                        else:
                            if item in ['Preemptive','Prepurchase','Preaccession'] and text_df[text_df.index(item)+3] in ['Split','Dividend', 'Other']:
                                del text_df[text_df.index(item)-3:text_df.index(item)+6]
                            else:
                                if item in ['Split','Dividend', 'Other'] and text_df[text_df.index(item)+2] in ['Split','Dividend', 'Other']:
                                    del text_df[text_df.index(item)-3:text_df.index(item)+5]
                                else:
                                    if item in ['Split','Dividend', 'Other']:
                                        del text_df[text_df.index(item)-3:text_df.index(item)+3]
                                    else:
                                        if item in ['Preemptive', 'Prepurchase', 'Preaccession']:
                                            del text_df[text_df.index(item)-3:text_df.index(item)+4]
                n = 11 #number of variables
                list_to_add = [text_df[i:i + n] for i in range(0, len(text_df), n)]
                list_to_df.append(list_to_add)
            
            else:
                pass
        
        except:
            pass
    
    #data pre-formatting
    flat_list = itertools.chain(*list_to_df)
    flat_list = list(flat_list)
    
    stock_df = pd.DataFrame(flat_list, columns = ['No', 'day','mon', 'year', 'open', 'high', 'low', 'close', 'perc_change',
                                                   'abs_change', 'vol'])
    stock_df['Ticker'] = ticker
    stock_df.loc[stock_df.No == '1', 'vol'] = stock_df.loc[stock_df.No == '1', 'perc_change']
    stock_df.loc[stock_df.No == '1', 'perc_change'] = None
    
    wig_stocks = wig_stocks.append(stock_df)

#dates reformatting
def dates_format(df):
    df.loc[df.mon == 'Dec', 'mon'] = '12'
    df.loc[df.mon == 'Mar', 'mon'] = '03'
    df.loc[df.mon == 'Jun', 'mon'] = '06'
    df.loc[df.mon == 'Sep', 'mon'] = '09'
    df["period"] = df["day"] +'-'+ df["mon"] +'-'+ df["year"]
    df.drop(['day','mon','year'], axis = 1, inplace = True)
    return df

wig_stocks = dates_format(wig_stocks)

#save to csv
wig_stocks.to_csv('D:/UW/4 semester/Empirics/project/wig_stocks.csv') 