#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random
import seaborn as sns
import os
import pandas as pd
import numpy as np
import openpyxl
import matplotlib.pyplot as plt
from datetime import date as conv_date
get_ipython().run_line_magic('matplotlib', 'inline')
pd.set_option('mode.chained_assignment', None)

def data_analysis(savefolder,
                  savename_comp,
                  savename_hist_data,
                  savename_basic_calc,
                  savename_portf_analysis,
                  savename_optimize_portf,
                  corr_table,
                  perf_compare_table):
    """
    Basic statistics tables, correlation matric and performance comparison
    on a randomly generated portfolio
    """
    sp_500 = pd.read_excel(os.path.join(savefolder, savename_comp),
                           usecols = "A:C")

    time_series = pd.read_excel(os.path.join(savefolder, savename_hist_data),
                                index_col = "Date",
                                parse_dates = True)

    # 1 # Log returns per product
    log_returns = pd.DataFrame()

    for i in time_series.columns:
        log_returns[i] = np.log(time_series[i] / time_series[i].shift(1))
        
    log_returns.index = [conv_date(x.year, x.month, x. day) for x in time_series.index]
    log_returns.index.name = "Date"
    log_returns = log_returns.iloc[1:]
    
    # 2 # full data table
    stock_lvl_calc = log_returns.agg(["mean", "std", "max", "min"]).transpose().reset_index()
    stock_lvl_calc.columns = stock_lvl_calc.columns.str.replace("index", "Symbol")

    stock_lvl_calc["Annualized_mean_yield"] = stock_lvl_calc["mean"] * 250
    stock_lvl_calc["Annualized_std"] = stock_lvl_calc["std"] * np.sqrt(250)

    stock_lvl_calc = stock_lvl_calc.merge(sp_500,
                                          how = "left",
                                          on = "Symbol")

    stock_lvl_calc =     (stock_lvl_calc
         .drop(columns = ["mean", "std"])
         .set_index("Symbol")
         .rename(columns = {"max": "Max_daily_yield",
                            "min": "Min_daily_yield",
                            "Annualized_mean_yield": "Annualized_mean_yield",
                            "Annualized_std": "Annualized_std",
                            "Security": "Security_name",
                            "GICS_Sector": "Sector"})
         .filter(['Security_name',
                  'Sector',
                  'Max_daily_yield',
                  'Min_daily_yield',
                  'Annualized_mean_yield',
                  'Annualized_std']))

    stock_lvl_calc["Sector"].iloc[0] = "Market_index"
    stock_lvl_calc["Security_name"].iloc[0] = "SP500_index"

    # 3 # Sector level calc
    sector_level = stock_lvl_calc.groupby("Sector").agg({"Max_daily_yield": "max",
                                                         "Min_daily_yield": "min",
                                                         "Annualized_mean_yield": ["max", "mean"],
                                                         "Annualized_std": ["max", "mean"]})

    # 4 # Best performers
    best_performers = pd.DataFrame(stock_lvl_calc.groupby("Sector")["Annualized_mean_yield"].nlargest(3))
    best_performers.query('Sector != "Market_index"', inplace = True)

    with pd.ExcelWriter(os.path.join(savefolder, savename_basic_calc), engine='xlsxwriter') as writer:
        log_returns.to_excel(writer, sheet_name = 'daily_returns', freeze_panes = (1,2))
        stock_lvl_calc.to_excel(writer, sheet_name = "asset_lvl_calculation", freeze_panes = (1,1))
        sector_level.to_excel(writer, sheet_name = 'sector_lvl_calculation')
        best_performers.to_excel(writer, sheet_name = 'top_performers_per_sector')
    
    print(f"File with basic calculation named {savename_basic_calc} has been saved down:\n - 'daily_returns'tab: logarithmic returns for all asset (S&P500 index and its components)\n - 'asset_lvl_calculation' tab: Asset level return and standard deviation results\n - 'sector_lvl_calculation' tab: Sector level statistics\n - 'top_performers_per_sector' tab: Top 3 performer symbols listed by sectors.\n")
    
    # 5 # Correlation heatmap
    sectors = set(sp_500["GICS_Sector"])
    random_portf = []

    for i in sectors:
        random_portf.append(random.sample(list(sp_500[sp_500["GICS_Sector"] == i]["Symbol"]), 1))

    random_portf = ["^GSPC"] + list(np.array(random_portf).flatten())

    random_portfolio = log_returns.filter(items = random_portf)

    corr = random_portfolio.corr()

    # Advanced vizulalization
    fig, ax = plt.subplots(figsize=(12,10))

    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    ax = sns.heatmap(corr.round(2), mask=mask, ax=ax, annot=True, annot_kws={'fontsize':10}, cmap="RdYlGn")
    ax.set_xticklabels(ax.xaxis.get_ticklabels(), fontsize=12)
    ax.set_yticklabels(ax.yaxis.get_ticklabels(), fontsize=12);

    plt.savefig(os.path.join(savefolder, corr_table))
    print(f"'{corr_table}' saved down")
    
    # 6 # Yield comparison in the randomly generated portfolio
    rand_portfolio = log_returns.filter(items = random_portfolio, axis = 1).cumsum()  # log yields can be summed up
    market_portfolio = rand_portfolio["^GSPC"]
    rand_shares = rand_portfolio.iloc[:, 1:]
    
    plt.figure(figsize=(18,10))
    plt.plot(rand_portfolio.index, market_portfolio, color='green', linewidth = 3)
    plt.plot(rand_portfolio.index, rand_shares, linewidth = 1)
    plt.grid(which = 'both', axis = 'y')
    plt.legend(rand_portfolio)
    plt.savefig(os.path.join(savefolder, perf_compare_table))
    print(f"'{perf_compare_table}' saved down")
    
    with pd.ExcelWriter(os.path.join(savefolder, savename_portf_analysis), engine='xlsxwriter') as writer2:
        corr.to_excel(writer2, sheet_name = "correlation_table", float_format = '%.4f')
        rand_portfolio.to_excel(writer2, sheet_name = "performance_comparison", float_format = '%.4f')
    
    print(f"\nRandom portfolio calculations are saved down ({savename_portf_analysis}):\n - 'correlation_table' tab: correlation table saved down with randomly chosen portfolio\n - 'performance_comparison' tab: performance comparison of S&P500 index and the random components\n")

