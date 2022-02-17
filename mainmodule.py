"""
@author: JutasiR
"""
# Standard library imports
import os
import time

# Third party imports
import numpy as np

# Local application imports
import basiccalculations.dataanalyzer as da
import portfoliocreation.portfoliogenerator as pg
import webscraping.webscraper as wb
from paramhandling import ParamHandler


def main_program():
    """Creates stock porfolio built from S&P500 elements"""
    savefolder: str = os.path.join(os.getcwd(), "output_folder\\")
    savename_comp: str = "1_sp_500_elements.xlsx"
    savename_hist_data: str = "1_times_series_us_stocks.xlsx"
    savename_basic_calc: str = "2_basic_calculations.xlsx"
    savename_portf_analysis: str = "2_rand_portfolio_measures.xlsx"
    corr_table: str = "2_correlation_table.png"
    perf_compare_table: str = "2_performance_comparison.png"
    savename_optimize_portf: str = "3_portfolio_optimization_results.xlsx"
    portfolios_chart = "3_Efficient_frontier.png"

    params = ParamHandler()

    print("\nPART I. - Parameter definition\n")

    ans1 = input(
        "Would you like to see the parameter names, their default values and descriptions? (Y/N)? "
    )

    if ans1.lower() == "y":
        params.get_parameter_description()

    ans2 = input("\nWould you like to change the input parameters? (Y/N)? ")

    if ans2.lower() == "y":
        print(
            "\nPlease input the parameters as whole numbers, default values are given in the brackets!"
        )

        nr_of_years = int(input("Number of years, the tenor of historical data (5): "))
        stock_nr = int(
            input("Number of stocks chosen during the portfolio generation (7): ")
        )
        nr_of_modeled_portf = int(
            input("Number of randomly chosen set of stocks /portfolio/ (1000): ")
        )
        nr_of_weights_per_portf = int(
            input("Number of randomly generated weights in all set of stocks (800): ")
        )

    else:
        nr_of_years = params.nr_of_years
        stock_nr = params.stock_nr
        nr_of_modeled_portf = params.nr_of_modeled_portf
        nr_of_weights_per_portf = params.nr_of_weights_per_portf

    if not os.path.exists(savefolder):
        os.mkdir(savefolder)

    start_total = time.perf_counter()

    print("\nPART II. - Web scraping\n")

    wb.save_data_from_web(nr_of_years, savefolder, savename_comp, savename_hist_data)

    print("PART III. - Basic data analysis\n")

    da.data_analysis(
        savefolder,
        savename_comp,
        savename_hist_data,
        savename_basic_calc,
        savename_portf_analysis,
        corr_table,
        perf_compare_table,
    )

    print("PART IV. - Portfolio generation\n")

    pg.portfolio_creator_usd_stocks(
        stock_nr,
        nr_of_modeled_portf,
        nr_of_weights_per_portf,
        savename_hist_data,
        savefolder,
        portfolios_chart,
        savename_optimize_portf,
    )

    end_total = time.perf_counter() - start_total
    print(
        "Overall Run time: {0} min {1} sec\n".format(
            int(np.round(end_total // 60, 0)), int(np.round(end_total % 60, 0))
        )
    )


if __name__ == "__main__":
    main_program()
