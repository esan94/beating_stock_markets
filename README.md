# BEATING STOCK MARKETS #

1. **bsm_categorical_data**
2. **exploring_data**
3. **data**


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
 
 In this section we find a notebook called *categorical_data_exploratory.ipynb* which is an exploratory analysis about *db_bsm_categorical.csv*. To see the analysis you could:
 1. Copy the HTML code in *categorical_data_exploratory.html* in a .txt file changing the extension to .html.
 2. Clone the repo and run the html
 3. Clone the repo and deploy all notebook in a anaconda workspace.
 
 
 # IN PROGRESS
 
