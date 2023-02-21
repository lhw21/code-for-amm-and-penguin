# This script is used to calculate the area of the MIZ
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ross_data = np.load('Ross_nisdc_sic_dataset_197811_202112.npy')
ross_data = ross_data[2:,:,:]

winter_data_ross = np.zeros((129,132,316))*np.nan
for i_new in range(43):
    winter_data_ross[(i_new*3):(i_new*3+3),:,:] = ross_data[(i_new*12+5):(i_new*12+8),:,:]

winter_data_ross = winter_data_ross[:,:,120:180]
# plt.imshow(winter_data_ross[0,:,:])

MIZ_data=[]
for i in range(129): 
    
    plot_data = winter_data_ross[i,:,:]
    plot_data[plot_data<=15]=0
    plot_data[plot_data>=80]=0
    
    fig=plt.figure()
    plt.title(str(i))
    ax1=fig.add_subplot(121)
    ax1.imshow(plot_data,cmap='bwr')

    for col in range(plot_data.shape[1]):
        temp_data=plot_data[:,col]
        temp_data=np.nan_to_num(temp_data)
        index=np.where(temp_data>=15)
        max_index=index[0][-1] 
        
        temp_data[max_index+1:]=np.nan
        
        index2=np.where(temp_data==0)

        index2 = np.array(index2)
        index2 = np.reshape(index2, (np.shape(index2)[1],))
        b = np.flipud(index2) 
        for t in range(len(b)-2):
            f1 = b[t]
            f2 = b[t+1]*2
            f3 = b[t+2]
            if f2 == f1+f3:
                temp_data[:f1+1]=np.nan
                break
        
        plot_data[:,col]=temp_data
        
    MIZ_data.append(np.sum(~np.isnan(plot_data)))
        
    ax1=fig.add_subplot(122)
    ax1.imshow(plot_data,cmap='bwr')
    
    plt.savefig('test'+str(i)+'.png',dpi=300)
    
MIZ_data = np.array(MIZ_data)
MIZ_data1=np.reshape(MIZ_data,(43,3))
MIZ_data2=pd.DataFrame(MIZ_data1)
MIZ_data2.to_excel('MIZ.xlsx')