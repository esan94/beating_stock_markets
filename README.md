# BEATING STOCK MARKETS #
 
1. **bsm_categorical_data**
2. **exploring_data**
3. **bsm_financial_data**
4. **bsm_models**
5. **data**
6. **models, models_f_classif & models_mutual**


### bsm_categorical_data

In this section there is the code to download categorical data from [yahoo finance](https://finance.yahoo.com/).
The description about data is:
- ticker: Column with the name of the company in a stock market.
- company: Column with the name of the company.
- sector_gics: Column with the standard sectors for companies from [GICS](https://en.wikipedia.org/wiki/Global_Industry_Classification_Standard).
- sector_icb: Column with the standard sectors for companies from [ICB](https://en.wikipedia.org/wiki/https://en.wikipedia.org/wiki/Industry_Classification_Benchmark).
- country: Column with the country of the company.

The downloading data is save in the folder data with name db_bsm_categorical.csv.

To deploy this software, first of all it has to clone this repo and then install all needed dependencies with `pip install -r requirements.txt` in a virtual
environment or in the core. And finally to run script open a terminal in the folder *bsm_categorical_data* and type `python launch.py`. 

There are a parameter inside the *launch.py* called **IS_DEBUG_MODE** that is `False`. If you change to `True` you will have in the folder *data* all intermediates dataframes
 as csv used to build the last data base (in csv) named *db_bsm_categorical.csv*.
 
### exploring_data
 
 In this section we find a notebook called *categorical_data_exploratory.ipynb* which is an exploratory analysis about *db_bsm_categorical.csv*. Also a rmd called *financial_data_exploratory.rmd* which is an exploratory analysis of *db_bsm_financial.csv* and a time series analysis of the *db_bsm_financial.csv* where I decompose the close time 
 serie in seasonality, trend and deploy an ARIMA among other analysis as well. Also you could find a notebook called models_viz.ipynb which is to visualize
 the precission of the models and preparing_data_4visualization.ipynb that is to preparing the data to create the dashboads in Tableau.To see these analysis you could:
 
 1. Copy the HTML files in a .txt file changing the extension to .html.
 2. Clone the repo and run the html.
 3. Clone the repo and deploy all notebook in a anaconda workspace. For the .rmd you need R statistic.
 
 
 ### bsm_financial_data
 
 In this section there is the code to download all financial data from [Alpha Vantage](https://www.alphavantage.co/). The description of the data is:
 
- ticker: Column with the name of the company in a stock market.
- close: Close price of the market for a company and a day.
- date: Daily price of the company in the stock market.
- volume: Number of transactions
- ADX: Average directional index [click](https://en.wikipedia.org/wiki/Average_directional_movement_index)
- Aroon: [click](https://www.investopedia.com/terms/a/aroon.asp)
- BOP: Balance of power [click](https://tradingsim.com/blog/balance-of-power/)
- CCI: Commodity channel index [click](https://www.investopedia.com/articles/active-trading/031914/how-traders-can-utilize-cci-commodity-channel-index-trade-stock-trends.asp)
- CMO: Chande momentum oscilator [click](https://www.investopedia.com/terms/c/chandemomentumoscillator.asp)
- Chaikin A/D: Chaikin oscillator [click](https://www.investopedia.com/articles/active-trading/031914/understanding-chaikin-oscillator.asp)
- DEMA: Double exponential moving average [click](https://www.investopedia.com/articles/trading/10/double-exponential-moving-average.asp)
- DX: Directional movement [click](https://www.investopedia.com/terms/d/dmi.asp)
- FAMA: Fractal adaptative moving average [click](https://www.metatrader5.com/es/terminal/help/indicators/trend_indicators/fama)
- KAMA: Kaufman's adaptative moving average [click](http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:kaufman_s_adaptive_moving_average)
- MACD: Moving average convergence divergence [click](https://www.investopedia.com/terms/m/macd.asp)
- MAMA: MESA Adaptative moving average [click](https://www.tradingview.com/script/foQxLbU3-Ehlers-MESA-Adaptive-Moving-Average-LazyBear/)
- MINUS_DI: Negative directional indicator [click](https://www.investopedia.com/terms/n/negativedirectionalindicator.asp)
- MINUS_DM: Directional movement [click](https://www.tradingview.com/wiki/Directional_Movement_(DMI))
- MOM: Momentum [click](https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/momentum-mom/)
- NATR: Normalized average true range [click](https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/normalized-average-true-range-natr/)
- OBV: On-Balance volumen [click](https://www.investopedia.com/terms/o/onbalancevolume.asp)
- PLUS_DM: Directional movement [click](https://www.tradingview.com/wiki/Directional_Movement_(DMI))
- PLUS_DI: Positive directional indicator [click](https://www.investopedia.com/terms/n/negativedirectionalindicator.asp)
- PPO: Porcentage price oscillator [click](https://www.investopedia.com/terms/p/ppo.asp)
- ROCR: Rate of change [click](https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/rate-of-change-rocr/)
- RSI: Relative strenght index [click](https://www.investopedia.com/terms/r/rsi.asp)
- BBands: Bolinger bands [click](https://en.wikipedia.org/wiki/Bollinger_Bands)
- SAR: [click](https://www.investopedia.com/trading/introduction-to-parabolic-sar/)
- SMA: Simple moving average [click](https://www.investopedia.com/terms/s/sma.asp)
- SlowDK: Stochastic oscillator [click](https://www.investopedia.com/terms/s/stochasticoscillator.asp)
- WMA: Weighted moving average [click](https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/weighted-moving-average-wma/)
- ULTOSC: Ultimate oscillator [click](https://www.investopedia.com/terms/u/ultimateoscillator.asp)

There are columns with a number in the name this means the period in the calculate data.

### bsm_models
 
In this section there is the code to make all models in function of the day to predict and the sector_gics.
Here is where the model is deployed and there is a parameter called `feature_selection` in the folder models and the
script launch.py whose values could be 'mutual', 'f_classif' or None and decide which feature extraction do before the train part.

### data

Here is where all data from AlphaVantage, yahoo finance or processed are saved.

### models, models_f_classif & models_mutual

In this section we can find the trained models from bsm_models for each feature extraction.


