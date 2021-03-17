#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
@author: JutasiR
"""
import os
import random as r
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def portfolio_creator_usd_stocks(stock_nr,
                                 nr_of_modeled_portf,
                                 nr_of_weights_per_portf,
                                 savename_hist_data,
                                 savefolder,
                                 portfolios_chart,
                                 savename_optimize_portf):

    """
    - Generates multiple portfolios as per given attributes by random choices
    (nr_of_modeled_portf)
    - The random combinations are the run with different weights per security, generated randomly
    (nr_of_weights_per_portf)
    - Element number in the portfolio: stock_nr

    IMPORTANT: The same return bearing portfolios with higher volatility is removed

    """
    data = pd.read_excel(os.path.join(savefolder, savename_hist_data), index_col = [0])
    tickers = set(data.columns)
    log_return = np.log(data / data.shift(1))

    portfolio_ret = []
    portfolio_vol =  []
    portfolio_weights = []
    portfolio_elements = []
    
    total = nr_of_weights_per_portf * nr_of_modeled_portf
    print("Portfolio generation starts...")
    print(f"Nr of portfolio randomly created: {total}")
    
    for _ in range(nr_of_modeled_portf):
        chosen = r.sample(tickers, stock_nr)

        for i in range(nr_of_weights_per_portf):

            weights = (np.random.random(stock_nr))
            weights /= np.sum(weights)
            portfolio_ret.append(round(np.sum(weights * log_return[chosen].mean() * 250), 4))
            portfolio_vol.append(round(np.sqrt(np.dot(weights.T,np.dot(log_return[chosen].cov()*250, weights))), 6))
            portfolio_weights.append(list(weights))
            portfolio_elements.append(chosen)

    portfolio_ret = np.array(portfolio_ret)
    portfolio_vol = np.array(portfolio_vol)

    portfolios = pd.DataFrame({"Return" : portfolio_ret,
                               "Volatility" : portfolio_vol,
                               "Weights" : portfolio_weights,
                               "Elements" : portfolio_elements})

    # In case of same return portfolios, the lower vol. bearing is kept, the others (now below it) are deleted
    portfolios.sort_values(by = ["Return", "Volatility"], ascending = [0, 1], inplace = True)
    portfolios["Return_shifted"] = portfolios["Return"].shift(1)
    
    portfolios =         portfolios[portfolios.apply(lambda portfolios: portfolios["Return"] != portfolios["Return_shifted"], axis=1)]
    
    portfolios.drop(columns = "Return_shifted", inplace = True)

    portfolios[["Return", "Volatility"]].plot(x = "Volatility",
                                              y = "Return",
                                              kind = "scatter",
                                              figsize = (13,9))

    plt.xlabel("Expected Volatility")
    plt.ylabel("Expected Return")
    plt.savefig(os.path.join(savefolder, portfolios_chart))
    print(f"Results are saved down as a scatter chart named as'{portfolios_chart}'\n")
    
    pd.DataFrame(portfolios).to_excel(os.path.join(savefolder, savename_optimize_portf), index = False)

