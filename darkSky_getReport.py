

# tool to get dark sky weather reports from the DarkSky 'Time Machine API'

'''

myKey = '829db48b2456dfdc17f17c637add698b'

Request format
    https://api.darksky.net/forecast/[key]/[latitude],[longitude],[time]

Example
    GET https://api.darksky.net/forecast/0123456789abcdef9876543210fedcba/42.3601,-71.0589,409467600?exclude=currently,flags

'''


import json
import pandas as pd
import urllib.request


# pass a darksky url string and returns a data frame of weather info!
def get_weather_data(zipcode, url):

    # submit get request to url
    with urllib.request.urlopen(url) as URL:
        weather_dict = json.loads(URL.read().decode())


    # flatted dict to hourly rows
    weather_data_records_list = []
    for data_record in weather_dict['hourly']['data']:

        # print('=' * 80)
        d = {}
        # appent record variables
        d['zipcode'] = zipcode
        d['latitude'] = weather_dict['latitude']
        d['longitude'] = weather_dict['longitude']
        d['timezone'] = weather_dict['timezone']
        d['offset'] = weather_dict['offset']
        d['daily_summary'] = weather_dict['hourly']['summary']
        d['daily_icon'] = weather_dict['hourly']['icon']

        # loop over values in item
        for k, v in data_record.items():
            d[str(k)] = str(v)
            d[str(k)] = str(v)

        # append dictionart to weather_report_list
        weather_data_records_list.append(d)

    # convert list of dictionaries to a DataFrame
    weather_df = pd.DataFrame(weather_data_records_list)

    return weather_df



station_coords = [   '37.32973200,-121.90178200', '37.33069800,-121.88897900', '37.33398800,-121.89490200', '37.33141500,-121.89320000', '37.33672100,-121.89407400',
                    '37.33379800,-121.88694300', '37.33016500,-121.88583100', '37.34874200,-121.89471500', '37.33739100,-121.88699500', '37.33588500,-121.88566000',
                    '37.33280800,-121.88389100', '37.33930100,-121.88993700', '37.33269200,-121.90008400', '37.33395500,-121.87734900', '37.48175800,-122.22690400',
                    '37.48607800,-122.23208900', '37.48850100,-122.23106100', '37.48421900,-122.22742400', '37.48672500,-122.22555100', '37.48768200,-122.22349200',
                    '37.38921800,-122.08189600', '37.39435800,-122.07671300', '37.40694000,-122.10675800', '37.39027700,-122.06655300', '37.40044300,-122.10833800',
                    '37.38595600,-122.08367800', '37.40024100,-122.09907600', '37.44398800,-122.16475900', '37.44452100,-122.16309300', '37.42908200,-122.14280500',
                    '37.44859800,-122.15950400', '37.42568390,-122.13777750', '37.78387100,-122.40843300', '37.79500100,-122.39997000', '37.79728000,-122.39843600',
                    '37.79423100,-122.40292300', '37.79542500,-122.40476700', '37.78897500,-122.40345200', '37.79995300,-122.39852500', '37.78962500,-122.39026400',
                    '37.79539200,-122.39420300', '37.79146400,-122.39103400', '37.78715200,-122.38801300', '37.78975600,-122.39464300', '37.79225100,-122.39708600',
                    '37.78175200,-122.40512700', '37.77865000,-122.41823500', '37.78133200,-122.41860300', '37.80477000,-122.40323400', '37.78052600,-122.39028800',
                    '37.78529900,-122.39623600', '37.78697800,-122.39810800', '37.78225900,-122.39273800', '37.77105800,-122.40271700', '37.77481400,-122.41895400',
                    '37.77661900,-122.41738500', '37.78487800,-122.40101400', '37.77637700,-122.39607000', '37.77661700,-122.39526000', '37.78844600,-122.40849900',
                    '37.78035600,-122.41291900', '37.79852200,-122.40724500', '37.79413900,-122.39443400', '37.79130000,-122.39905100', '37.78630500,-122.40496600',
                    '37.78962500,-122.40081100', '37.35260100,-121.90573300', '37.79854100,-122.40086200', '37.49126900,-122.23623400', '37.34272500,-121.89561700',
                    '37.48761600,-122.22995100', '37.48537000,-122.20328800', '37.79030200,-122.39063700', '37.77660000,-122.39547000', '37.78103900,-122.41174800',
                    '37.33239800,-121.89042900', '37.33195700,-121.88163000', '37.79790000,-122.40594200', '37.78014800,-122.40315800', '37.78590800,-122.40889100',
                    '37.39533700,-122.05247600', '37.42090900,-122.08062300']
zips = ['94041', '94063', '94107', '94301', '95113']
zip_coords = [  [94041, 37.388520, -122.075726],
                [94063, 37.493297, -122.195535],
                [94107, 37.760460, -122.399724],
                [94301, 37.444123, -122.149911],
                [95113, 37.333694, -121.891002]]



day_interval = 86400

start_hour = '08/28/2013 12:06:01'
start_hour_epoch = 1377673200

end_hour = '09/01/2016 00:00:00.00'
end_hour_epoch = 1472713200

days = range(start_hour_epoch, end_hour_epoch+day_interval, day_interval)

myKey = '829db48b2456dfdc17f17c637add698b'






url_list = []

time = str(1377673200)

for z in zip_coords:

    zipcode = str(z[0])
    lat = str(z[1])
    lon = str(z[2])

    # test_url = 'https://api.darksky.net/forecast/829db48b2456dfdc17f17c637add698b/37.32973200,-121.90178200,1502268691?exclude=currently,minutely,daily,flags'

    formatted_url = 'https://api.darksky.net/forecast/' + myKey + '/' + lat + ',' + lon + ',' + time + '?exclude=currently,minutely,daily,flags'

    url_list.append([zipcode, formatted_url])





weather = pd.DataFrame()
chunks = []

for entry in url_list:
    zipcode = entry[0]
    weatherURL = entry[1]
    chunk = get_weather_data(zipcode, weatherURL)

    chunks.append(chunk)


weather = pd.concat(chunks)


#------------------------------------------------------------------------------
#   Data Cleanup
#------------------------------------------------------------------------------

# Fill NaN values with zeros
weather[['cloudCover', 'uvIndex']] = weather[['cloudCover', 'uvIndex']].fillna(0)



# stations['station_id'] = stations['station_id'].astype(int)

weather['apparentTemperature'] = weather['apparentTemperature'].astype(float)
weather['cloudCover'] = weather['cloudCover'].astype(float)
weather['dewPoint'] = weather['dewPoint'].astype(float)
weather['humidity'] = weather['humidity'].astype(float)
weather['latitude'] = weather['latitude'].astype(float)
weather['longitude'] = weather['longitude'].astype(float)
weather['precipIntensity'] = weather['precipIntensity'].astype(float)
weather['precipProbability'] = weather['precipProbability'].astype(float)
weather['pressure'] = weather['pressure'].astype(float)
weather['temperature'] = weather['temperature'].astype(float)
weather['uvIndex'] = weather['uvIndex'].astype(float)
weather['visibility'] = weather['visibility'].astype(float)
weather['windSpeed'] = weather['windSpeed'].astype(float)

# weather['time_adj'] = pd.to_datetime(weather['time'],unit='s')
# weather['time_adj'] = weather['time_adj'] + pd.to_timedelta(weather.offset, unit='h')

weather['time_adj'] = pd.to_datetime(weather['time'],unit='s') + pd.to_timedelta(weather.offset, unit='h')


# prune down to just the columns we want to use
important_cols = ['daily_summary', 'summary', 'zipcode', 'apparentTemperature', 'cloudCover', 'latitude', 'longitude', 'precipIntensity', 'precipProbability', 'temperature', 'time_adj']
weather = weather[important_cols]

['daily_summary', 'summary', 'zipcode', 'apparentTemperature', 'cloudCover', 'latitude', 'longitude', 'precipIntensity', 'precipProbability', 'temperature', 'time_adj']




print(weather.head())
print(weather.info())
print(weather.describe())


# write dataframe to csv




filename = 'sample_weather.csv'
weather.to_csv(filename, index=False, encoding='utf-8')


# EOF
