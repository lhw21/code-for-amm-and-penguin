# This script is used to calculate the correlation between the Adélie penguin population 
# and the AMM index

import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import scipy.signal as signal
import scipy.stats as st

# function that calculates lag correlation
def lag_cal(year_list, peng_series, AMM_timeseries, lag):
    # year_list：list of years of penguin populations observation
    # peng_series: penguin population series
    # AMM_timeseries: AMM index series
    # lag: lag year
    year_temp = np.array(year_list)
    year_temp = year_temp-lag
    AMM_temp = AMM_timeseries.loc[year_temp,'annual']
    cor,pvalue = pearsonr(peng_series, AMM_temp)
    return cor,pvalue

# Read the penguin population series
adelie_obnum = np.load('adelie_obnum.npy',allow_pickle=True).item()
# list of colony names
sn = list(adelie_obnum.keys())
# Read the year_list
adelie_year = np.load('adelie_year.npy',allow_pickle=True).item()

# Read the AMM index series
AMM_df = pd.read_csv('amm_de_norm.csv')
AMM_series = AMM_df.set_index('Year')

# Create new tables to store Corr and Pvalue
ini_corr = np.zeros((8,23))*np.nan
ini_pvalue = np.zeros((8,23))*np.nan
ini_corr = pd.DataFrame(ini_corr)
ini_pvalue = pd.DataFrame(ini_pvalue)
ini_corr.columns = sn
ini_corr.index = [0,1,2,3,4,5,6,7]
ini_pvalue.columns = sn
ini_pvalue.index = [0,1,2,3,4,5,6,7]

for site in sn:
    for lag_year in [0,1,2,3,4,5,6,7]:
        peng_num = adelie_obnum[site]
        year = adelie_year[site]
        # Delinear trend of penguin sequences
        slope, intercept, _, _, _ = st.linregress(year, peng_num)
        peng_num_dtrend = peng_num - (np.array(year)*slope+intercept)
        
        r,p = lag_cal(year, peng_num_dtrend, AMM_series, lag_year)
        ini_corr.loc[lag_year,site] = r
        ini_pvalue.loc[lag_year,site] = p

ini_corr.to_excel('corr_amm_adelie_reanalysis.xlsx')
ini_pvalue.to_excel('pvalue_amm_adelie_reanalysis.xlsx')