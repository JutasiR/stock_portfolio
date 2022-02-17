"""
@author: JutasiR
"""

# Standard library imports
import random
import seaborn as sns
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date as conv_date

get_ipython().run_line_magic("matplotlib", "inline")
pd.set_option("mode.chained_assignment", None)


def data_analysis(
    savefolder,
    savename_comp,
    savename_hist_data,
    savename_basic_calc,
    savename_portf_analysis,
    corr_table,
    perf_compare_table,
):
    """
    Basic statistics tables, correlation matric and performance comparison
    on a randomly generated portfolio
    """
    sp_500 = pd.read_excel(os.path.join(savefolder, savename_comp), usecols="A:C")

    time_series = pd.read_excel(
        os.path.join(savefolder, savename_hist_data), index_col="Date", parse_dates=True
    )

    log_returns = log_returns_calc(time_series)

    stock_lvl_calc = full_data_table_create(log_returns, sp_500)

    sector_level = sector_level_calc(stock_lvl_calc)

    best_performers = best_performers_per_industry(stock_lvl_calc)

    with pd.ExcelWriter(
        os.path.join(savefolder, savename_basic_calc), engine="xlsxwriter"
    ) as writer:
        log_returns.to_excel(writer, sheet_name="daily_returns", freeze_panes=(1, 2))
        stock_lvl_calc.to_excel(
            writer, sheet_name="asset_lvl_calculation", freeze_panes=(1, 1)
        )
        sector_level.to_excel(writer, sheet_name="sector_lvl_calculation")
        best_performers.to_excel(writer, sheet_name="top_performers_per_sector")

    print(
        f"File with basic calculation named {savename_basic_calc} has been saved down:\n - 'daily_returns'tab: logarithmic returns for all asset (S&P500 index and its components)\n - 'asset_lvl_calculation' tab: Asset level return and standard deviation results\n - 'sector_lvl_calculation' tab: Sector level statistics\n - 'top_performers_per_sector' tab: Top 3 performer symbols listed by sectors\n"
    )

    sectors = set(sp_500["GICS_Sector"])

    correlation_table, random_portfolio_performance = random_portfolio_tables(
        sectors, sp_500, log_returns, time_series, savefolder, savename_portf_analysis
    )

    random_portf_charts(
        correlation_table,
        random_portfolio_performance,
        savefolder,
        corr_table,
        perf_compare_table,
    )


def log_returns_calc(time_series):
    # 1 # Log returns per product
    log_returns = pd.DataFrame()

    for i in time_series.columns:
        log_returns[i] = np.log(time_series[i] / time_series[i].shift(1))

    log_returns.index = [conv_date(x.year, x.month, x.day) for x in log_returns.index]
    log_returns.index.name = "Date"
    log_returns = log_returns.iloc[1:]

    return log_returns


def full_data_table_create(log_returns, sp_500):

    stock_lvl_calc = (
        log_returns.agg(["mean", "std", "max", "min"]).transpose().reset_index()
    )
    stock_lvl_calc.columns = stock_lvl_calc.columns.str.replace("index", "Symbol")

    stock_lvl_calc["Annualized_mean_yield"] = stock_lvl_calc["mean"] * 250
    stock_lvl_calc["Annualized_std"] = stock_lvl_calc["std"] * np.sqrt(250)

    stock_lvl_calc = stock_lvl_calc.merge(sp_500, how="left", on="Symbol")

    stock_lvl_calc = (
        stock_lvl_calc.drop(columns=["mean", "std"])
        .set_index("Symbol")
        .rename(
            columns={
                "max": "Max_daily_yield",
                "min": "Min_daily_yield",
                "Annualized_mean_yield": "Annualized_mean_yield",
                "Annualized_std": "Annualized_std",
                "Security": "Security_name",
                "GICS_Sector": "Sector",
            }
        )
        .filter(
            [
                "Security_name",
                "Sector",
                "Max_daily_yield",
                "Min_daily_yield",
                "Annualized_mean_yield",
                "Annualized_std",
            ]
        )
    )

    stock_lvl_calc["Sector"].iloc[0] = "Market_index"
    stock_lvl_calc["Security_name"].iloc[0] = "SP500_index"

    return stock_lvl_calc


def sector_level_calc(stock_lvl_calc):

    sector_level = stock_lvl_calc.groupby("Sector").agg(
        {
            "Max_daily_yield": "max",
            "Min_daily_yield": "min",
            "Annualized_mean_yield": ["max", "mean"],
            "Annualized_std": ["max", "mean"],
        }
    )

    return sector_level


def best_performers_per_industry(stock_lvl_calc):

    best_performers = pd.DataFrame(
        stock_lvl_calc.groupby("Sector")["Annualized_mean_yield"].nlargest(3)
    )
    best_performers.query('Sector != "Market_index"', inplace=True)

    return best_performers


def random_portfolio_tables(
    sectors, sp_500, log_returns, time_series, savefolder, savename_portf_analysis
):

    random_portf = []

    for i in sectors:
        random_portf.append(
            random.sample(list(sp_500[sp_500["GICS_Sector"] == i]["Symbol"]), 1)
        )

    random_portf_elements = ["^GSPC"] + list(np.array(random_portf).flatten())

    random_portfolio_returns = log_returns.filter(items=random_portf_elements)
    correlation_table = random_portfolio_returns.corr()

    random_portfolio_prices = time_series.filter(items=random_portf_elements)
    random_portfolio_performance = 100 * (
        random_portfolio_prices / random_portfolio_prices.iloc[0]
    )

    random_portfolio_performance[
        "Equal_weighted_rand_portf"
    ] = random_portfolio_performance.iloc[:, 1:].mean(axis=1)

    random_portfolio_performance.index = [
        conv_date(x.year, x.month, x.day) for x in random_portfolio_performance.index
    ]
    random_portfolio_performance.index.name = "Date"

    with pd.ExcelWriter(
        os.path.join(savefolder, savename_portf_analysis), engine="xlsxwriter"
    ) as writer2:
        correlation_table.to_excel(
            writer2, sheet_name="correlation_table", float_format="%.4f"
        )
        random_portfolio_performance.to_excel(
            writer2, sheet_name="performance_comparison", float_format="%.4f"
        )

    print(
        f"Random portfolio calculations are saved down ({savename_portf_analysis}):\n - 'correlation_table' tab: correlation table saved down with randomly chosen portfolio\n - 'performance_comparison' tab: performance comparison of S&P500 index and the random components\n"
    )

    return correlation_table, random_portfolio_performance


def random_portf_charts(
    correlation_table,
    random_portfolio_performance,
    savefolder,
    corr_table,
    perf_compare_table,
):

    print("Saving down the charts:")
    # Correlation_table
    fig, ax = plt.subplots(figsize=(12, 10))

    mask = np.zeros_like(correlation_table, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    ax = sns.heatmap(
        correlation_table.round(2),
        mask=mask,
        ax=ax,
        annot=True,
        annot_kws={"fontsize": 10},
        cmap="RdYlGn",
    )
    ax.set_xticklabels(ax.xaxis.get_ticklabels(), fontsize=12)
    ax.set_yticklabels(ax.yaxis.get_ticklabels(), fontsize=12)

    plt.savefig(os.path.join(savefolder, corr_table))
    print(f" - '{corr_table}' saved down")

    market_portfolio = random_portfolio_performance["^GSPC"]
    rand_shares = random_portfolio_performance.iloc[:, 1:-1]
    equal_weighted_rand_portf = random_portfolio_performance.iloc[:, -1:]

    plt.figure(figsize=(18, 10))
    plt.plot(
        random_portfolio_performance.index, market_portfolio, color="green", linewidth=3
    )
    plt.plot(
        random_portfolio_performance.index, rand_shares, linestyle="--", linewidth=2
    )
    plt.plot(
        random_portfolio_performance.index,
        equal_weighted_rand_portf,
        color="blue",
        linewidth=3,
    )
    plt.grid(which="both", axis="y")
    plt.legend(random_portfolio_performance)
    plt.title("S&P500 vs random portfolio and its components")
    plt.savefig(os.path.join(savefolder, perf_compare_table))
    print(f" - '{perf_compare_table}' saved down\n")
