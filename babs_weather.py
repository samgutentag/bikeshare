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

#   change zip to int
# df_weather['zip'] = df_weather['zip'].astype(int)

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

# print('#' * 80)
# print('#\tHEAD')
# print(df_weather.head())

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

# # plot the min_temp and max_temp weather data as a scatter plot
# df_weather.groupby('zip').plot(kind='scatter', x='min_temp', y='max_temp')
# plt.xlabel='min_temp (F)'
# plt.ylabel='max_temp (F)'
# plt.show()


# #   plot mean_temp by zip
color_list = ['red', 'green', 'blue', 'orange', 'yellow']
counter = 0
fig, ax = plt.subplots(figsize=(8,6))
for label, df in df_weather.groupby('zip'):
    df.plot(kind='scatter', c=color_list[counter], x='min_temp', y='max_temp', ax=ax, label=label, alpha=0.3)
    counter += 1
plt.legend()
plt.xlabel='min_temp (F)'
plt.ylabel='max_temp (F)'
plt.show()




# #   plot mean_temp by zip
fig, ax = plt.subplots(figsize=(8,6))
for label, df in df_weather.groupby('zip'):

    df_mean_temp = df['mean_temp']
    df_mean_temp = df_mean_temp.resample('W').mean()
    df_mean_temp.plot(kind="line", ax=ax, label=label)

plt.legend()
plt.show()


#   EOF
