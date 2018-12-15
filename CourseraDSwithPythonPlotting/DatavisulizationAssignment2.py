
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

if __name__=='__main__':

    weatherData = pd.read_csv('C:/Users/ksdee/Downloads/assgn2-data.csv')


    weatherData['Year'] = weatherData['Date'].apply(lambda x: int(x[:4]))
    weatherData['Month'] = weatherData['Date'].apply(lambda x: int(x[5:7]))
    weatherData['Day'] = weatherData['Date'].apply(lambda x: int(x[8:10]))

    weatherData2015 = weatherData[weatherData['Year'] == 2015]

    weatherData.drop(weatherData[(weatherData['Month'] == 2) & (weatherData['Day'] == 29)].index, axis=0, inplace=True)
    weatherData = weatherData.loc[(weatherData['Year']>=2005) & (weatherData['Year']<=2014)]

    groupedweatherData = weatherData.groupby(by=['Date', 'Element'])
    groupedweatherData = groupedweatherData['Data_Value'].agg([np.max, np.min])
    groupedweatherData.reset_index(inplace=True)

    minTempData = groupedweatherData.loc[groupedweatherData['Element'] == 'TMIN', ['Date', 'amin']]
    maxTempData = groupedweatherData.loc[groupedweatherData['Element'] == 'TMAX', ['Date', 'amax']]

    minMaxData = pd.merge(minTempData,maxTempData,how='outer',on='Date')
    minMaxData['Date']=[pd.Timestamp(dt.datetime.strptime(str(x), '%Y-%m-%d')) for x in minMaxData['Date'].values]
    minMaxDate = minMaxData['Date'].dt.to_pydatetime()
    fig = plt.figure()
    fig.set_size_inches(23.125, 13.125)
    plt.plot(minMaxDate, minMaxData['amin'], 'b', label='Record Minimum Temperature')
    plt.plot(minMaxDate, minMaxData['amax'], 'r', label='Record Maximum Temperature')
    plt.fill_between(minMaxDate, minMaxData['amin'], minMaxData['amax'],
                     facecolor='yellow', alpha=1, interpolate=True)



    weatherData2015['Date'] = [pd.Timestamp(dt.datetime.strptime(str(x), '%Y-%m-%d')) for x in weatherData2015['Date'].values]

    groupedweatherData2015 = weatherData2015.groupby(by=['Date', 'Element'])
    groupedweatherData2015 = groupedweatherData2015['Data_Value'].agg([np.max, np.min])
    groupedweatherData2015.reset_index(inplace=True)

    minTempData2015 = groupedweatherData2015.loc[groupedweatherData2015['Element'] == 'TMIN', ['Date', 'amin']]
    maxTempData2015 = groupedweatherData2015.loc[groupedweatherData2015['Element'] == 'TMAX', ['Date', 'amax']]

    maxTempPnt = np.max(maxTempData2015['amax'])
    minTempPnt = np.min(minTempData2015['amin'])

    weatherData['Date'] = [pd.Timestamp(dt.datetime.strptime(str(x), '%Y-%m-%d')) for x in weatherData['Date'].values]
    maxBreak = weatherData.loc[weatherData['Data_Value'] > maxTempPnt]
    minBreak = weatherData.loc[weatherData['Data_Value'] < minTempPnt]

    maxBreakDate = maxBreak['Date'].dt.to_pydatetime()
    minBreakDate = minBreak['Date'].dt.to_pydatetime()

    plt.scatter(maxBreakDate, maxBreak['Data_Value'], s=100, c='cyan', label='Broken highs of 2015')
    plt.scatter(minBreakDate, minBreak['Data_Value'], s=100, c='green' , label='Broken lows of 2015')

    plt.xlabel('Date in Years')
    # add a label to the y axis
    plt.ylabel('Temperature (tenths of degrees C)')
    # add a title
    plt.title('Temperature distribution for the region of Ann Arbor, Michigan, United States')
    plt.legend()

    plt.show()

    fig.savefig('C:/Users/ksdee/Downloads/plot.png')

