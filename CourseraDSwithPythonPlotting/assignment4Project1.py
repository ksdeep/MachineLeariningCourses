import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

import matplotlib.gridspec as gridspec



data=pd.read_csv('C:\\Users\\ksdee\\Downloads\\data.csv\\data2.csv',encoding='utf-8',header=0,low_memory=False, sep=',',error_bad_lines =False)
data['isMetro'] = [x in ['Delhi','Greater Mumbai','Mumbai','Chennai','Kolkata','Calcutta'] for x in data['location']]
data = data[data['isMetro']]
data.loc[data[data['location']=='Greater Mumbai'].index,'location'] = 'Mumbai'
data.loc[data[data['location'] == 'Calcutta'].index, 'location'] = 'Kolkata'
data['Year'] = data['date'].apply(lambda x: int(x[6:10]))
data['Month'] = data['date'].apply(lambda x: int(x[3:5]))
data['Day'] = data['date'].apply(lambda x: int(x[0:2]))


data['date'] = [pd.Timestamp(dt.datetime.strptime(str(x), '%d-%m-%Y')) for x in data['date'].values]
data = data[['location','so2','no2','pm2_5','date','Day','Month','Year']]

location ='Mumbai'
pollutant = 'so2'
saftSO2 = [50,80]
safeNO2 = [40,80]
safePM2_5 = [60,100]
alp =0.5



fig = plt.figure()
gspec = gridspec.GridSpec(2, 2)

so2plot = plt.subplot(gspec[0, 0])
no2plot = plt.subplot(gspec[1, 0])
pm2_5plot = plt.subplot(gspec[:, 1])



dataMumbaiSO2 = data.loc[data[data['location'] == 'Mumbai'].index, ['date','so2', 'Day','Month','Year']]
dataMumbaiSO2 = dataMumbaiSO2.dropna()
dataMumbaiSO2.sort_values('date',ascending =True, inplace=True)
groupedDataMumbaiSo2 = dataMumbaiSO2.groupby(by=['Year','Month'])
groupedDataMumbaiSo2 = groupedDataMumbaiSo2['so2'].agg([np.max])
groupedDataMumbaiSo2.reset_index(inplace=True)

dataKolkataSO2 = data.loc[data[data['location'] == 'Kolkata'].index,['date','so2', 'Day','Month','Year']]
dataKolkataSO2 = dataKolkataSO2.dropna()
dataKolkataSO2.sort_values('date',ascending =True, inplace=True)
groupedDataKolkataSO2 = dataKolkataSO2.groupby(by=['Year','Month'])
groupedDataKolkataSO2 = groupedDataKolkataSO2['so2'].agg([np.max])
groupedDataKolkataSO2.reset_index(inplace=True)



dataChennaiSO2 = data.loc[data[data['location'] == 'Chennai'].index,['date','so2', 'Day','Month','Year']]
dataChennaiSO2 = dataChennaiSO2.dropna()
dataChennaiSO2.sort_values('date',ascending =True, inplace=True)
groupedDataChennaiSO2 = dataChennaiSO2.groupby(by=['Year','Month'])
groupedDataChennaiSO2 = groupedDataChennaiSO2['so2'].agg([np.max])
groupedDataChennaiSO2.reset_index(inplace=True)


dataDelhiSO2 = data.loc[data[data['location'] == 'Delhi'].index,['date','so2', 'Day','Month','Year']]
dataDelhiSO2 = dataDelhiSO2.dropna()
dataDelhiSO2.sort_values('date',ascending =True, inplace=True)
groupedDataDelhiSO2 = dataDelhiSO2.groupby(by=['Year','Month'])
groupedDataDelhiSO2 = groupedDataDelhiSO2['so2'].agg([np.max])
groupedDataDelhiSO2.reset_index(inplace=True)




y = groupedDataMumbaiSo2['amax']
x ='1-'+groupedDataMumbaiSo2['Month'].astype(str)+'-'+groupedDataMumbaiSo2['Year'].astype(str)
x = x.apply(lambda x : dt.datetime.strptime(str(x), '%d-%m-%Y'))
# groupedDataMumbaiSo2.apply( lambda x: datetime.date(x[['Year']],x[['Month']],1))
# RMy = running_mean(np.array(y), 3)
# x = groupedDataMumbaiSo2['Month'].astype(str)+'-'+groupedDataMumbaiSo2['Year'].astype(str)
so2plot.plot(x, y,'-',color='orange', alpha=alp, marker="o", label='Mumbai')


y = groupedDataKolkataSO2['amax']
x ='1-'+groupedDataKolkataSO2['Month'].astype(str)+'-'+groupedDataKolkataSO2['Year'].astype(str)
x = x.apply(lambda x : dt.datetime.strptime(str(x), '%d-%m-%Y'))
so2plot.plot(x, y, '-',color='blue', alpha=alp, marker="o", label='Kolkata')

y = groupedDataChennaiSO2['amax']
x ='1-'+groupedDataChennaiSO2['Month'].astype(str)+'-'+groupedDataChennaiSO2['Year'].astype(str)
x = x.apply(lambda x : dt.datetime.strptime(str(x), '%d-%m-%Y'))
so2plot.plot(x, y, '-', color='green', alpha=alp, marker="o", label='Chennai')

y = groupedDataDelhiSO2['amax']
x ='1-'+groupedDataDelhiSO2['Month'].astype(str)+'-'+groupedDataDelhiSO2['Year'].astype(str)
x = x.apply(lambda x : dt.datetime.strptime(str(x), '%d-%m-%Y'))
so2plot.plot(x, y, '-', color='cyan', alpha=alp, marker="o", label='Delhi')

ytick = so2plot.get_yticks()
ytick = ytick[ytick >= 0]
so2plot.set_yticks(list(ytick) + saftSO2)
so2plot.set_title('Monthly Maximum recorded SO2 ')
so2plot.spines['right'].set_visible(False)
so2plot.spines['top'].set_visible(False)
so2plot.spines['bottom'].set_visible(False)
so2plot.spines['left'].set_visible(False)
so2plot.axhline(saftSO2[0], linestyle='-', color='g')
so2plot.axhline(saftSO2[1], linestyle='-', color='r')
so2plot.annotate('Healthy', [x[len(x) - 1], int(saftSO2[0] / 2)-10])
so2plot.annotate('Moderate', [x[len(x) - 1], int(saftSO2[0] + (saftSO2[1] - saftSO2[0]) / 2)-10])
so2plot.annotate('UnHealthy', [x[len(x) - 1], int(saftSO2[1] + saftSO2[1] / 2)+10])
so2plot.set_ylabel('SO2 (micro Gram per Meter cube)')
so2plot.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=True,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off
so2plot.xaxis.grid(True)
so2plot.yaxis.grid(True)



#-----------------------------

dataMumbaiNO2 = data.loc[data[data['location'] == 'Mumbai'].index, ['date','no2', 'Day','Month','Year']]
dataMumbaiNO2 = dataMumbaiNO2.dropna()
dataMumbaiNO2.sort_values('date',ascending =True, inplace=True)
groupedDataMumbaiNO2 = dataMumbaiNO2.groupby(by=['Year','Month'])
groupedDataMumbaiNO2 = groupedDataMumbaiNO2['no2'].agg([np.max])
groupedDataMumbaiNO2.reset_index(inplace=True)

dataKolkataNO2 = data.loc[data[data['location'] == 'Kolkata'].index,['date','no2', 'Day','Month','Year']]
dataKolkataNO2 = dataKolkataNO2.dropna()
dataKolkataNO2.sort_values('date',ascending =True, inplace=True)
groupedDataKolkataNO2 = dataKolkataNO2.groupby(by=['Year','Month'])
groupedDataKolkataNO2 = groupedDataKolkataNO2['no2'].agg([np.max])
groupedDataKolkataNO2.reset_index(inplace=True)



dataChennaiNO2 = data.loc[data[data['location'] == 'Chennai'].index,['date','no2', 'Day','Month','Year']]
dataChennaiNO2 = dataChennaiNO2.dropna()
dataChennaiNO2.sort_values('date',ascending =True, inplace=True)
groupedDataChennaiNO2 = dataChennaiNO2.groupby(by=['Year','Month'])
groupedDataChennaiNO2 = groupedDataChennaiNO2['no2'].agg([np.max])
groupedDataChennaiNO2.reset_index(inplace=True)


dataDelhiNO2 = data.loc[data[data['location'] == 'Delhi'].index,['date','no2', 'Day','Month','Year']]
dataDelhiNO2 = dataDelhiNO2.dropna()
dataDelhiNO2.sort_values('date',ascending =True, inplace=True)
groupedDataDelhiNO2 = dataDelhiNO2.groupby(by=['Year','Month'])
groupedDataDelhiNO2 = groupedDataDelhiNO2['no2'].agg([np.max])
groupedDataDelhiNO2.reset_index(inplace=True)




y = groupedDataMumbaiNO2['amax']
x ='1-'+groupedDataMumbaiNO2['Month'].astype(str)+'-'+groupedDataMumbaiNO2['Year'].astype(str)
x = x.apply(lambda x : dt.datetime.strptime(str(x), '%d-%m-%Y'))
no2plot.plot(x, y,'-',color='orange', alpha=alp, marker="o", label='Mumbai')


y = groupedDataKolkataNO2['amax']
x ='1-'+groupedDataKolkataNO2['Month'].astype(str)+'-'+groupedDataKolkataNO2['Year'].astype(str)
x = x.apply(lambda x : dt.datetime.strptime(str(x), '%d-%m-%Y'))
no2plot.plot(x, y, '-',color='blue', alpha=alp, marker="o", label='Kolkata')

y = groupedDataChennaiNO2['amax']
x ='1-'+groupedDataChennaiNO2['Month'].astype(str)+'-'+groupedDataChennaiNO2['Year'].astype(str)
x = x.apply(lambda x : dt.datetime.strptime(str(x), '%d-%m-%Y'))
no2plot.plot(x, y, '-', color='green', alpha=alp, marker="o", label='Chennai')

y = groupedDataDelhiNO2['amax']
x ='1-'+groupedDataDelhiNO2['Month'].astype(str)+'-'+groupedDataDelhiNO2['Year'].astype(str)
x = x.apply(lambda x : dt.datetime.strptime(str(x), '%d-%m-%Y'))
no2plot.plot(x, y, '-', color='cyan', alpha=alp, marker="o", label='Delhi')

ytick = no2plot.get_yticks()
ytick = ytick[ytick >= 0]
no2plot.set_yticks(list(ytick) + safeNO2)
no2plot.set_title('Monthly Maximum recorded NO2 ')
no2plot.spines['right'].set_visible(False)
no2plot.spines['top'].set_visible(False)
no2plot.spines['bottom'].set_visible(False)
no2plot.spines['left'].set_visible(False)
no2plot.axhline(safeNO2[0], linestyle='-', color='g')
no2plot.axhline(safeNO2[1], linestyle='-', color='r')
no2plot.annotate('Healthy', [x[len(x) - 1], int(safeNO2[0] / 2)-10])
no2plot.annotate('Moderate', [x[len(x) - 1], int(safeNO2[0] + (safeNO2[1] - safeNO2[0]) / 2)-10])
no2plot.annotate('UnHealthy', [x[len(x) - 1], int(safeNO2[1] + safeNO2[1] / 2)+10])
no2plot.set_ylabel('NO2 (micro Gram per Meter cube)')
no2plot.xaxis.grid(True)
no2plot.yaxis.grid(True)

#--------------------------------------------------------

dataMumbaiPM2_5 = data.loc[data[data['location'] == 'Mumbai'].index, ['date','pm2_5', 'Day','Month','Year']]
dataMumbaiPM2_5 = dataMumbaiPM2_5.dropna()
dataMumbaiPM2_5.sort_values('date',ascending =True, inplace=True)
groupedDataMumbaiPM2_5 = dataMumbaiPM2_5.groupby(by=['Year','Month'])
groupedDataMumbaiPM2_5 = groupedDataMumbaiPM2_5['pm2_5'].agg([np.max])
groupedDataMumbaiPM2_5.reset_index(inplace=True)

dataKolkataPM2_5 = data.loc[data[data['location'] == 'Kolkata'].index,['date','pm2_5', 'Day','Month','Year']]
dataKolkataPM2_5 = dataKolkataPM2_5.dropna()
dataKolkataPM2_5.sort_values('date',ascending =True, inplace=True)
groupedDataKolkataPM2_5 = dataKolkataPM2_5.groupby(by=['Year','Month'])
groupedDataKolkataPM2_5 = groupedDataKolkataPM2_5['pm2_5'].agg([np.max])
groupedDataKolkataPM2_5.reset_index(inplace=True)



dataChennaiPM2_5 = data.loc[data[data['location'] == 'Chennai'].index,['date','pm2_5', 'Day','Month','Year']]
dataChennaiPM2_5 = dataChennaiPM2_5.dropna()
dataChennaiPM2_5.sort_values('date',ascending =True, inplace=True)
groupedDataChennaiPM2_5 = dataChennaiPM2_5.groupby(by=['Year','Month'])
groupedDataChennaiPM2_5 = groupedDataChennaiPM2_5['pm2_5'].agg([np.max])
groupedDataChennaiPM2_5.reset_index(inplace=True)


dataDelhiPM2_5 = data.loc[data[data['location'] == 'Delhi'].index,['date','pm2_5', 'Day','Month','Year']]
dataDelhiPM2_5 = dataDelhiPM2_5.dropna()
dataDelhiPM2_5.sort_values('date',ascending =True, inplace=True)
groupedDataDelhiPM2_5 = dataDelhiPM2_5.groupby(by=['Year','Month'])
groupedDataDelhiPM2_5 = groupedDataDelhiPM2_5['pm2_5'].agg([np.max])
groupedDataDelhiPM2_5.reset_index(inplace=True)




y = groupedDataMumbaiPM2_5['amax']
x ='1-'+groupedDataMumbaiPM2_5['Month'].astype(str)+'-'+groupedDataMumbaiPM2_5['Year'].astype(str)
x = x.apply(lambda x : dt.datetime.strptime(str(x), '%d-%m-%Y'))
pm2_5plot.plot(x, y,'-',color='orange', alpha=alp, marker="o", label='Mumbai')


y = groupedDataKolkataPM2_5['amax']
x ='1-'+groupedDataKolkataPM2_5['Month'].astype(str)+'-'+groupedDataKolkataPM2_5['Year'].astype(str)
x = x.apply(lambda x : dt.datetime.strptime(str(x), '%d-%m-%Y'))
pm2_5plot.plot(x, y, '-',color='blue', alpha=alp, marker="o", label='Kolkata')

y = groupedDataChennaiPM2_5['amax']
x ='1-'+groupedDataChennaiPM2_5['Month'].astype(str)+'-'+groupedDataChennaiPM2_5['Year'].astype(str)
x = x.apply(lambda x : dt.datetime.strptime(str(x), '%d-%m-%Y'))
pm2_5plot.plot(x, y, '-', color='green', alpha=alp, marker="o", label='Chennai')

y = groupedDataDelhiPM2_5['amax']
x ='1-'+groupedDataDelhiPM2_5['Month'].astype(str)+'-'+groupedDataDelhiPM2_5['Year'].astype(str)
x = x.apply(lambda x : dt.datetime.strptime(str(x), '%d-%m-%Y'))
pm2_5plot.plot(x, y, '-', color='cyan', alpha=alp, marker="o", label='Delhi')

ytick = pm2_5plot.get_yticks()
ytick = ytick[ytick >= 0]
pm2_5plot.set_yticks(list(ytick) + safePM2_5)
pm2_5plot.set_title('Monthly Maximum recorded PM2_5 ')
pm2_5plot.spines['right'].set_visible(False)
pm2_5plot.spines['top'].set_visible(False)
pm2_5plot.spines['bottom'].set_visible(False)
pm2_5plot.spines['left'].set_visible(False)
pm2_5plot.axhline(safePM2_5[0], linestyle='-', color='g')
pm2_5plot.axhline(safePM2_5[1], linestyle='-', color='r')
pm2_5plot.annotate('Healthy', [x[len(x) - 1], int(safePM2_5[0] / 2)-10])
pm2_5plot.annotate('Moderate', [x[len(x) - 1], int(safePM2_5[0] + (safePM2_5[1] - safePM2_5[0]) / 2)-10])
pm2_5plot.annotate('UnHealthy', [x[len(x) - 1], int(safePM2_5[1] + safePM2_5[1] / 2)+10])
pm2_5plot.set_ylabel('PM2.5 (micro Gram per Meter cube)')
pm2_5plot.xaxis.grid(True)
pm2_5plot.yaxis.grid(True)
pm2_5plot.legend(loc='upper corner', fontsize='small')


plt.show()

