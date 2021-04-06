#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
@author: JutasiR
"""

# Standard library imports
import os
import time
import pandas as pd
import numpy as np
from pandas_datareader import data as web
import datetime as dt

def sp_components(savefolder,
                  savename):

    print("Downloading the component data of S&P500...")
    tables = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    sp_500_data = tables[0]
    sp_500_data.columns = [str(x).strip() for x in sp_500_data.columns]
    sp_500_data.columns = sp_500_data.columns.str.replace("GICS Sector", "GICS_Sector")
    
    (sp_500_data
         .filter(["Symbol", "Security", "GICS_Sector"])
         .to_excel(os.path.join(savefolder, savename),
                   index = False,
                   freeze_panes = (1, 1)))
    
    print(f"S&P500 component table ({savename}) has been saved down")
    
    return ['^GSPC'] + [str(x).strip() for x in sp_500_data["Symbol"]]

def save_data_from_web(nr_of_years,
                       savefolder,
                       savename_comp,
                       savename_hist_data):

    new_year = dt.date.today().year - nr_of_years
    start_date = str(dt.date(new_year, dt.date.today().month, dt.date.today().day))
    
    data = pd.DataFrame()

    tickers = sp_components(savefolder, savename_comp)

    print("\nDownload of closing prices by ticker from the given date period from Yahoo...")
    for share in tickers:
        try:
            data[share] = web.DataReader(share, data_source = "yahoo", start = start_date)["Adj Close"]

        except:
            time.sleep(3)
            try:
                data[share] = web.DataReader(share, data_source = "yahoo", start = start_date)["Adj Close"]
            except:
                print(" - {0} cannot be loaded".format(share))
                continue
    
    data.index = [dt.date(date.year, date.month, date.day) for date in data.index]
    data.index.name = "Date"
    
    (data
        .fillna(method = 'ffill', axis = 'index')
        .dropna(how = 'any', axis = 'columns')
        .to_excel(os.path.join(savefolder, savename_hist_data),
                  index = True,
                  freeze_panes = (1, 1)))
    
    print(f"\nTime series ({savename_hist_data}) has been saved down\n")


# In[ ]:




