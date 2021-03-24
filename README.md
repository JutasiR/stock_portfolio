# stock_portfolio

This project aims to be a basic portfolio investment tool using fundamental financial methodologies with the help of Python.
It is planned to be expanded to 6 or 7 modules overall depending on the number topics related.

As per the latest update, the following modules are ready to use (the 'mainmodule' runs all of these in order):
1. 'webscraper.py': S&P500 index and its components are downloaded from wikipedia (tickers), than the historical closing prices* are saved down using the tickers.
2. 'dataanalyzer.py': Basic statistics and calculations (log return, standard deviation, random portfolio generation, correlation matrix, asset performance comparison)
3. 'portfoliogenerator.py': huge number of random portfolio generated to create the 'efficient frontier': these are the best portfolios with highest yield on a certain level of volatility (measure for riskiness) or the lowest level of volatility on a certain level of return.

Other files in the project folder:
- 'requirements.txt': to create a virtual enviroment that contains the necessary libraries (I added some extra packages that will be used in the later modules)
- 'paramhandling.py': contains a class that reads and uses the configuration file
- 'input_parameters.ini': the configuration file created

Upon running the 'mainmodule.py', the class is imported and the user can ask for information/description about the parameters exported from the config file as well as their default values. Should she/he require to alter the default values, the option is given during the runtime, please refrain from editting the 'input_parameters.ini' file. 

The results are saved down in a separate folder named 'output folder' in the working directory (the program automatically creates it, no need to manually do it).

In case you have any advice, questions or suggestions, please feel free to contact me at jutasiroland89@gmail.com.

***The results are not to be taken as an investment advice, they serve only as an introduction of basic financial principals and their application using Python 3.8.***

* Adjusted closing prices are used: https://help.yahoo.com/kb/SLN28256.html?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAABWqXx3Ulo6ZFu6sPRrqPpPvYeSvV9a2ZFr9tVBi4U4wTGgBFmJQ7CSati-97jUHcspAkRzrnQBiousTuVJ3mRiQa6r9gc1FMGkTOM30qrYtCCXBCGgJs4Im-O6DiyIHT0YnojgI2ROBfoLgrCwxn3gVH0miLv4B1R84EcZUrgKJ
