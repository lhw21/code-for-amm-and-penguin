# This script is used to calculate the area of sea ice in winter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sic_dat = np.load('Ross_nisdc_sic_dataset_197811_202112.npy')
sic_ross = sic_dat[2:,:,120:180] # Sea ice data after 1979

sie_area_list = []
for i in range(516):
    temp_flag = sic_ross[i,:,:]>=15
    num_up15 = np.sum(temp_flag)
    area_up15 = num_up15*25*25
    sie_area_list.append(area_up15)

sie_area_arr = np.array(sie_area_list)
sie_area_arr = np.reshape(sie_area_arr,(43,12))
sie_area_arr = pd.DataFrame(sie_area_arr)

cols = ['Jan','Feb','Mar','Apr',
        'May','Jun','Jul','Aug',
        'Sept','Oct','Nov','Dec']
index = list(np.arange(1979,2022))

sie_area_arr.columns = cols
sie_area_arr.index = index

sie_area_arr.to_excel('sie_ross_1979to2021.xlsx')
