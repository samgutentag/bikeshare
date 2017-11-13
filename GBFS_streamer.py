import urllib.request
from datetime import datetime
import json
import os
from math import ceil, floor
import sched, time


import pandas as pd


def get_stream_json(feed_url="https://gbfs.fordgobike.com/gbfs/en/station_status.json",
                        time_zone='America/Los_Angeles',
                        time_adjustment=pd.Timedelta('00:00:00'),
                        time_adjust_forward=True):

    # make json request across network
    with urllib.request.urlopen(feed_url) as url:
        url_json_response = json.loads(url.read().decode())

    print('\tLast Updated\t%s' % datetime.fromtimestamp(url_json_response['last_updated']).strftime("%A, %B %d, %Y %H:%M:%S"))

    df = pd.DataFrame(url_json_response['data'])
    df.head()
    df = pd.concat([df.drop(['stations'], axis=1), df['stations'].apply(pd.Series)], axis=1)
    df['last_reported'] = pd.to_datetime(df['last_reported'],unit='s')


    # correct time_zone
    if time_adjust_forward:
        df['last_reported'] = df['last_reported'] + time_adjustment
    else:
        df['last_reported'] = df['last_reported'] - time_adjustment

    df.set_index('last_reported', inplace=True)
    df.tz_localize(time_zone)
    df.reset_index(inplace=True)

    return df

def df_to_csv(df, file_dir, file_path):

    # make sure directory exists
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    if os.path.exists(file_path):
        # append if already exists
        with open(file_path, 'a') as f:
            df.to_csv(f, index=False, header=False)
    else:
        # make a new file if not
        with open(file_path, 'w') as f:
            df.to_csv(f, index=False, header=True)

    return True


def stream_gbfs_feed_json_to_csv(feed_url="https://gbfs.fordgobike.com/gbfs/en/station_status.json",
                                    feed_service='babs',
                                    feed_name='system_status',
                                    time_zone='America/Los_Angeles',
                                    time_adjustment=pd.Timedelta('00:00:00'),
                                    time_adjust_forward = True,
                                    file_interval = 30):

    df = get_stream_json(feed_url=feed_url, time_zone=time_zone, time_adjustment=time_adjustment, time_adjust_forward=time_adjust_forward)

    # Timestamp file - down to ten minute intervals
    dt = datetime.now()
    m = floor(dt.minute/file_interval)*file_interval
    tstamp = '{:04d}{:02d}{:02d}{:02d}{:02d}'.format(dt.year, dt.month, dt.day, dt.hour, m)

    feed_service = feed_service.replace('_', '')

    file_dir = 'streamed_data/%s/' % (feed_service.lower())
    file_name = 'streamed_data/%s/%s_%s_data_%s.csv' % (feed_service.lower(),
                                                            feed_service.lower(),
                                                            feed_name.lower(),
                                                            tstamp)
    df_to_csv(df, file_dir, file_name)

    return True

def main():

    s = sched.scheduler(time.time, time.sleep)
    def do_something(sc,):

        cogo_feed_url = "https://gbfs.cogobikeshare.com/gbfs/en/station_status.json"
        print('[%s] - Fetching feed from \'%s\'...' % (datetime.now().time(), cogo_feed_url))
        try:
            stream_gbfs_feed_json_to_csv(cogo_feed_url,
                                            feed_service='cogo',
                                            feed_name=cogo_feed_url.split('/')[-1][:-5],
                                            time_zone = 'America/New_York',
                                            time_adjustment=pd.Timedelta('5:00:00'),
                                            time_adjust_forward=False)
        except:
            print('---- Something went wrong, moving on ----')


        babs_feed_url = "https://gbfs.fordgobike.com/gbfs/en/station_status.json"
        print('[%s] - Fetching feed from \'%s\'...' % (datetime.now().time(), babs_feed_url))
        try:
            stream_gbfs_feed_json_to_csv(babs_feed_url,
                                            feed_service='babs',
                                            feed_name=babs_feed_url.split('/')[-1][:-5],
                                            time_zone = 'America/Los_Angeles',
                                            time_adjustment=pd.Timedelta('8:00:00'),
                                            time_adjust_forward=False)
        except:
            print('---- Something went wrong, moving on ----')

        # Newy York City
        citybike_feed_url = "https://gbfs.citibikenyc.com/gbfs/en/station_status.json"
        print('[%s] - Fetching feed from \'%s\'...' % (datetime.now().time(), babs_feed_url))
        try:
            stream_gbfs_feed_json_to_csv(babs_feed_url,
                                            feed_service='citibike',
                                            feed_name=citybike_feed_url.split('/')[-1][:-5],
                                            time_zone = 'America/New_York',
                                            time_adjustment=pd.Timedelta('5:00:00'),
                                            time_adjust_forward=False)
        except:
            print('---- Something went wrong, moving on ----')


        # Boston, MA
        hubway_feed_url = "https://gbfs.thehubway.com/gbfs/en/station_status.json"
        print('[%s] - Fetching feed from \'%s\'...' % (datetime.now().time(), babs_feed_url))
        try:
            stream_gbfs_feed_json_to_csv(babs_feed_url,
                                            feed_service='hubway',
                                            feed_name=hubway_feed_url.split('/')[-1][:-5],
                                            time_zone = 'America/New_York',
                                            time_adjustment=pd.Timedelta('5:00:00'),
                                            time_adjust_forward=False)
        except:
            print('---- Something went wrong, moving on ----')

        # Washington, D.C.
        cabi_feed_url = "https://gbfs.capitalbikeshare.com/gbfs/en/station_status.json"
        print('[%s] - Fetching feed from \'%s\'...' % (datetime.now().time(), babs_feed_url))
        try:
            stream_gbfs_feed_json_to_csv(babs_feed_url,
                                            feed_service='divvy',
                                            feed_name=cabi_feed_url.split('/')[-1][:-5],
                                            time_zone = 'America/New_York',
                                            time_adjustment=pd.Timedelta('5:00:00'),
                                            time_adjust_forward=False)
        except:
            print('---- Something went wrong, moving on ----')

        # Chicago, IL
        divvy_feed_url = "https://gbfs.divvybikes.com/gbfs/en/station_status.json"
        print('[%s] - Fetching feed from \'%s\'...' % (datetime.now().time(), babs_feed_url))
        try:
            stream_gbfs_feed_json_to_csv(babs_feed_url,
                                            feed_service='divvy',
                                            feed_name=divvy_feed_url.split('/')[-1][:-5],
                                            time_zone = 'America/Chicago',
                                            time_adjustment=pd.Timedelta('6:00:00'),
                                            time_adjust_forward=False)
        except:
            print('---- Something went wrong, moving on ----')








        seconds = 60
        interval = INTERVAL
        print('\t[%s] - Waiting %s minutes to run again...\n' % (datetime.now().time(), interval))
        s.enter(interval*seconds, 1, do_something, (sc,))


    s.enter(0, 1, do_something, (s,))
    s.run()

    return True




if __name__ == '__main__':

    global INTERVAL
    INTERVAL = 5

    main()
