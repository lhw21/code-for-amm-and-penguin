# This script is used to calculate the regression 
# of the meteorological field to the AMM index
import scipy.stats as st
import pandas as pd
import numpy as np
from netCDF4 import Dataset

# Function 1: 
# Calculate the seasonal average of the weather field
# input：
# var_arr: meteorological field
# n_year: number of years
# n_lat, n_lon: the latitude and longitude dimensions of the variable array
# sea_flag: season
def cal_sea_amm(var_arr, n_year, n_lat,n_lon, sea_flag):
    sea_arr = np.zeros((n_year,n_lat,n_lon))*np.nan
    if sea_flag=='spring':
        for i in range(n_year):
            forth = 12*i+8
            latte = 12*i+11
            sea_arr[i,:,:] = np.nanmean(var_arr[forth:latte,:,:],axis=0)
            
    if sea_flag=='summer':
        for i in range(n_year):
            forth = 12*i+11
            latte = 12*i+14
            sea_arr[i,:,:] = np.nanmean(var_arr[forth:latte,:,:],axis=0)

    if sea_flag=='autumn':
        for i in range(n_year):
            forth = 12*i+2
            latte = 12*i+5
            sea_arr[i,:,:] = np.nanmean(var_arr[forth:latte,:,:],axis=0)
            
    if sea_flag=='winter':
        for i in range(n_year):
            forth = 12*i+5
            latte = 12*i+8
            sea_arr[i,:,:] = np.nanmean(var_arr[forth:latte,:,:],axis=0)
    
    return sea_arr

# Function 2: 
# Calculate the regression of the meteorological field to the AMM index
# input：
# sea_arr: the variable field corresponding to the season
# n_lat, n_lon: the latitude and longitude dimensions of the variable array
# AMM_df: AMM index series
# sea_flag: season
def cal_sl_pval(sea_arr, n_lat, n_lon, AMM_df,sea_flag):
    amm_temp = AMM_df[sea_flag]
    slope_arr = np.zeros((n_lat,n_lon))*np.nan
    pval_arr = np.zeros((n_lat,n_lon))*np.nan
    for j in range(n_lat):
        print(j)
        for k in range(n_lon):
            slope, _, _, p_value, _ = st.linregress(amm_temp, sea_arr[:,j,k])
            slope_arr[j,k] = slope
            pval_arr[j,k] = p_value
    
    return slope_arr, pval_arr

# Function 3: Calculation functions
def cal_main(var_arr, n_year, n_lat,n_lon, AMM_df, sea_flag):
    sea_arr = cal_sea_amm(var_arr, n_year, n_lat,n_lon, sea_flag)
    sea_s, sea_p = cal_sl_pval(sea_arr, n_lat, n_lon, AMM_df,sea_flag)
    
    return sea_s, sea_p


# Read the AMM index data
amm_id_df = pd.read_csv('amm_de_norm.csv')

# Read the meteorological field
var = 'msl'
dataset = Dataset(var+'.nc')
lon = dataset.variables['longitude'][:]
lat = dataset.variables['latitude'][:]
var_da = dataset.variables[var][:]


n_year = 52 
n_lat = 361
n_lon = 1440
data_arr = np.zeros((8,n_lat,n_lon))*np.nan


sea_flag = 'spring'
data_arr[0,:,:], data_arr[4,:,:] = cal_main(var_da, n_year, n_lat,n_lon, amm_id_df, sea_flag)

sea_flag = 'summer'
data_arr[1,:,:], data_arr[5,:,:] = cal_main(var_da, n_year, n_lat,n_lon, amm_id_df, sea_flag)

sea_flag = 'autumn'
data_arr[2,:,:], data_arr[6,:,:] = cal_main(var_da, n_year, n_lat,n_lon, amm_id_df, sea_flag)

sea_flag = 'winter'
data_arr[3,:,:], data_arr[7,:,:] = cal_main(var_da, n_year, n_lat,n_lon, amm_id_df, sea_flag)

np.save(var+'.npy',data_arr)
np.save('longitude.npy',lon)
np.save('latitude.npy',lat)

