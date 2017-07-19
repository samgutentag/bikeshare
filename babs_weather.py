

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#   Import stock data

#------------------------------------------------------------------------------
#   Load Data Sets
#------------------------------------------------------------------------------
print('Loading data...')

try:
    weather_path_01 = '../../datasets/bayareabikeshare/201402_weather_data.csv'
    df_weather_01 = pd.read_csv(weather_path_01, header=0)

    weather_path_02 = '../../datasets/bayareabikeshare/201408_weather_data.csv'
    df_weather_02 = pd.read_csv(weather_path_02, header=0)

    weather_path_03 = '../../datasets/bayareabikeshare/201508_weather_data.csv'
    df_weather_03 = pd.read_csv(weather_path_03, header=0)

    weather_path_04 = '../../datasets/bayareabikeshare/201608_weather_data.csv'
    df_weather_04 = pd.read_csv(weather_path_04, header=0)

    print('data loaded successfully!')
except:
    print('oops... something went wrong loading the data :(')


print('\n\n')


print('#' * 80)
#------------------------------------------------------------------------------
#   Data Prep
#------------------------------------------------------------------------------

print('Data cleanup started...')
# columns of df_wether_01 are named differently than the rest, set them to match
df_weather_01.columns = df_weather_02.columns

#   merge all dataframes into a giant weather frame
weather_frames = [df_weather_01, df_weather_02, df_weather_03, df_weather_04]
df_weather = pd.concat(weather_frames)

#   Trim down weather data to columns we care about
columns_wanted =    ['PDT', 'Max TemperatureF', 'Mean TemperatureF', 'Min TemperatureF', ' Mean Wind SpeedMPH',  'PrecipitationIn', ' CloudCover', 'Zip']
column_new_names =  ['date', 'max_temp', 'mean_temp', 'min_temp', 'mean_wind', 'precipitation', 'cloud_cover', 'zip']

#   slim down dataframe to just things we need
df_weather = df_weather.loc[:,columns_wanted]
df_weather.columns = column_new_names

#   convert date column to datetime objects
df_weather['date'] = pd.to_datetime(df_weather['date'])

#   use date column as index
df_weather = df_weather.set_index('date')

#   precipitation column has a special 'T' value for trace amounts of rain, set all of these to zero
df_weather.loc[df_weather['precipitation'] == 'T', 'precipitation'] = 0.

#   force all columns to be numerical values
df_weather['precipitation'] = pd.to_numeric(df_weather['precipitation'], errors='coerce')

print('\tComplete!')


print('#' * 80)
#------------------------------------------------------------------------------
#   Statistical Analysis
#------------------------------------------------------------------------------

#look at unique values in each column
print('#' * 80)
print('#\tColumns and unique values')
for col in column_new_names[1:]:
    print('Column : ' + col)
    print(pd.unique(df_weather[col]))
    print()

print('#' * 80)
print('#\tHEAD')
print(df_weather.head())

print('#' * 80)
print('#\tINFO')
print(df_weather.info())

print('#' * 80)
print('#\tDESCRIBE')
print(df_weather.describe())

print('#' * 80)
#------------------------------------------------------------------------------
#   Data Visualization
#------------------------------------------------------------------------------



# plot the min_temp and max_temp weather data as a scatter plot
df_weather.plot(kind='scatter', x='min_temp', y='max_temp')
plt.xlabel='min_temp (F)'
plt.ylabel='max_temp (F)'
plt.show()


df_weather['max_temp'].plot(color='r', legend=True)
df_weather['mean_temp'].plot(color='g', legend=True)
df_weather['min_temp'].plot(color='b', legend=True)
plt.title('Temperature over time')
plt.ylabel= 'Temperature (F)'
plt.show()


df_weather.plot(kind='scatter', x='cloud_cover', y='precipitation')
plt.xlabel='Cloud Cover'
plt.ylabel='Precipitation (In)'

plt.title('Cloud Cover vs Precipitation')

plt.show()




#   plot mean_temp by zip

zip_codes = [94107, 94063, 94301, 94041, 95113]

for zip in zip_codes:
    df_zip = df_weather[df_weather.zip == zip]
    df_mean_temp = df_zip['mean_temp']
    df_zip_smoothed = df_mean_temp.rolling(window=30).mean()

    # df_zip['mean_temp'].plot(legend=True)
    df_zip_smoothed.plot()
    plt.title('Temperature over time')
    plt.ylabel= 'Temperature (F)'
    plt.show()




#   EOF
