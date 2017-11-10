import urllib.request
from datetime import datetime
import json
import os
from math import ceil, floor
import sched, time

import pandas as pd




# cogo_system_feeds_url = 'https://gbfs.cogobikeshare.com/gbfs/gbfs.json'
# cogo_system_information_feed_url = "https://gbfs.cogobikeshare.com/gbfs/en/system_information.json"
# cogo_station_information_feed_url = "https://gbfs.cogobikeshare.com/gbfs/en/station_information.json"
# cogo_station_status_feed_url = "https://gbfs.cogobikeshare.com/gbfs/en/station_status.json"


def get_stream_json(feed_url):
    with urllib.request.urlopen(feed_url) as url:
        url_json_response = json.loads(url.read().decode())


    print('\tLast Updated\t%s' % datetime.fromtimestamp(url_json_response['last_updated']).strftime("%A, %B %d, %Y %H:%M:%S"))

    refresh_timer = int(url_json_response['ttl'])

    df = pd.DataFrame(url_json_response['data'])
    df.head()
    df = pd.concat([df.drop(['stations'], axis=1), df['stations'].apply(pd.Series)], axis=1)
    df['last_reported'] = pd.to_datetime(df['last_reported'],unit='s')


    # Correct timezone
    df['last_reported'] = df['last_reported'] - pd.Timedelta('05:00:00')
    df.set_index('last_reported', inplace=True)
    df.tz_localize('America/New_York')
    df.reset_index(inplace=True)

    return (df, refresh_timer)

def df_to_csv(df, filepath):

    if os.path.exists(filepath):
        # append if already exists
        with open(filepath, 'a') as f:
            df.to_csv(f, index=False, header=False)
    else:
        # make a new file if not
        with open(filepath, 'w') as f:
            df.to_csv(f, index=False, header=True)


def stream_gbfs_feed_json_to_csv(feed_url, feed_service='SERVICE', feed_name='FEED'):

    df, refresh_timer = get_stream_json(feed_url)

    if refresh_timer < 10:
        refresh_timer = 15
    else:
        refresh_timer += 5


    # Timestamp file
    dt = datetime.now()
    m = floor(dt.minute/5)*5
    tstamp = '{:04d}{:02d}{:02d}{:02d}{:02d}'.format(dt.year, dt.month, dt.day, dt.hour, m)
    file_name = 'streamed_data/%s/station_status_data_%s.csv' % (feed_service.lower(), tstamp)
    file_name = 'streamed_data/%s/%s_%s_data_%s.csv' % (feed_service.lower(), feed_service.lower(), feed_name.lower(), tstamp)
    df_to_csv(df, file_name)

    return refresh_timer




def main():

    s = sched.scheduler(time.time, time.sleep)
    def do_something(sc):

        cogo_feed_url = "https://gbfs.cogobikeshare.com/gbfs/en/station_status.json"
        babs_feed_url = "https://gbfs.fordgobike.com/gbfs/en/station_status.json"

        feed_url = babs_feed_url
        program_name = 'babs'
        feed_name = 'station_status'


        print('[%s] - Fetching feed from \'%s\'...' % (datetime.now().time(), feed_url))
        refresh_timer = stream_gbfs_feed_json_to_csv(feed_url, feed_service=program_name, feed_name=feed_name)
        seconds = 60
        minutes = 5
        refresh_timer = minutes*seconds
        print('\t[%s] - Waiting %s minutes to run again...\n' % (datetime.now().time(), minutes))
        s.enter(refresh_timer, 1, do_something, (sc,))


    s.enter(0, 1, do_something, (s,))
    s.run()




if __name__ == '__main__':
    main()
