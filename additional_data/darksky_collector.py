# Collect dark sky forcast data to csv files

import os
import urllib.request
import json

import pandas as pd


# get DarkSky API Key

DARKSKY_KEY = os.environ.get('DARKSKY_KEY')
print(DARKSKY_KEY)


# load api calls file:
api_calls_file = './clean_data/darksky_api_calls.csv'
with open (api_calls_file, "r") as myfile:
    api_calls = myfile.readlines()

def get_forecast(_url):

    # make json request across network
    df = pd.DataFrame()
    try:
        with urllib.request.urlopen(_url) as url:
            url_json_response = json.loads(url.read().decode())
    except:
        print('\tURL %s had no response, skipping...' % _url)
        return False

    # parse hourly data from json response
    df_hourly = pd.DataFrame(url_json_response['hourly'])

    # split 'data' column of dictionary into separate rows
    df_hourly_details = df_hourly['data'].apply(pd.Series)

    # drop column, no longer needed
    df_hourly.drop('data', axis=1, inplace=True)

    # merge details into results
    forecast = df_hourly.merge(df_hourly_details, left_index=True, right_index=True)

    # extract components of forecast url result
    df = pd.DataFrame(url_json_response)
    df.transpose()
    forecast['latitude'] = df.latitude[0]
    forecast['longitude'] = df.longitude[0]
    forecast['offset'] = df.offset[0]

    forecast.rename(columns={'icon_x': 'daily_icon', 'summary_x': 'daily_summary',
                             'icon_y': 'hourly_icon', 'summary_y': 'hourly_summary'}, inplace=True)

    forecast['time_corrected'] = forecast.time + (3600 * forecast.offset)
    forecast['time_corrected'] = pd.to_datetime(forecast['time_corrected'],unit='s')


    # write to csv

    fn_y = str(list(forecast.time_corrected.dt.year.unique())[0]).zfill(4)
    fn_m = str(list(forecast.time_corrected.dt.month.unique())[0]).zfill(2)
    fn_d = str(list(forecast.time_corrected.dt.day.unique())[0]).zfill(2)

    lon = str(list(forecast.longitude.unique())[0]).replace('.', '').replace('-', '')
    filename = './source_data/darksky/%s%s%s_%s.csv' % (fn_y, fn_m, fn_d, lon)
    print('\t%s' % filename)

    forecast.to_csv(filename)

    return forecast

subset = api_calls[:]

total_calls = len(subset)
spacing = len(str(total_calls)) + 1

for i, c in enumerate(subset):
    _url = str(c).strip()[1:-1]
    print('%s of %s - %s' % (str(i+1).rjust(spacing), str(total_calls).rjust(spacing), _url))
    get_forecast(_url)
