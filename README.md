# Bay Area Bike Share Ridership
This project uses data reported by the Bay Area Bike Share (currently Ford Go Bike) program in San Francisco, California and surrounding Bay Area cities.

The Bay Area Bike Share Program was revamped and rebranded to Ford Go Bike in 2017 and has expanded its reach

# Results
The best Sub Topic Groupings were generated using an Online Latent Dirichlet Allocation model provided by `genesis`.  This Model was trained to identify 50 Topics, with 10 Terms per topic, and given 50 Passes to process the review texts.

Text was tokenized and lemmatized, so that we retained complete English readable words (vs stemming).  The corpus was restricted to only tokens appearing more frequently than the 10,000th most frequently token.  Example	 if the 10,000th token appeared just 3 times, only tokens occurring 4 or more times were kept.

This processing took nearly 13 hours to complete on a 2010 MacBook Pro, so please take that into consideration when attempting to recreate these results.

## Identified Sub Topics


## Assigning Topics to Reviews

## Calculating Restaurant Sub Topic Stars

## Identifying the Most Influential Sub Topics

## Comparison Reporting Tool


# Reproduce my Work
Few simple steps to get started and reproduce my work.

## Getting Started
Clone this repo to get started.  From there, if you are using `conda` to manage your virtual environment, run the following command to setup the environment and install the needed packages.  Be sure to pass the included `environment.yml` file.

```
# conda env create environment.yml
```

## Prerequisites
### Directory Structure

Once you have your environment set up, you will need to create some extra directories for your files.

### Env Variables

google maps API
darksky API


```
# python -m nltk.downloader all
# python -m spacy download en
```

Lastly, the data used for this project is supplied by the [Yelp Open Dataset](https://www.yelp.com/dataset).  You will need to download a copy of the source data and store it in a directory called `source_data` to run these notebooks without making changes to any code.

Specifically, you will need to copy over `business.json` and `review.json` from the downloaded data set to the `source_data` directory.

The starter directory structure should look like this:

```
yelpsubtopics
| -README.md
| -environment.yml
| -.gitignore
| -models
| -clean_data
| -source_data
|   |- business.json
|   |- review.json
| -documents
| -DataWrangling
|   |- 00_Business_Data_Wrangling.ipynb
|   |- 01_Review_Wrangling.ipynb
| -TopicModelling
|   |- model_03a_all_reviews_nouns.ipynb
|   |- model_05_all_reviews.ipynb
|   |- model_02_nff_reviews.ipynb
|   |- MODEL_SUMMARY.ipynb
|   |- model_01_ff_reviews.ipynb
|   |- model_04_all_reviews_nouns_verbs.ipynb
| -SubTopicReviews
|   |- SubTopicTagging_Model5.ipynb
|   |- SubTopic_Investigation.ipynb
|   |- plottingtools
|       |- init__.py
| -scripts
|   |- clean_checkins.py
|   |- clean_users.py
| -charts
|   |- reports
```

## Step 00 - Data Wrangling
Each of the provided data sets is moderately well formatted and abides by the [Global Bike Share Feed Specification](https://github.com/NABSA/gbfs) for data presentation.

Each Data Table is saved to a python pickle output file, so that data frames and column dtypes are preserved.


### Stations Data

<p>The stations data is in a collection of 4 files, each including the status of all stations that are active at the time the data was collected.  Additionally, Bay Area Bike Share published a `README.txt` file with each data set that includes notes on station expansion and relocation dates.</p>
<ol>
    <li>For each station, drop duplicated rows, reported when a station does not move or change between data collection times.</li>
    <li>Next we attend to each note included in the `README` files provided by the Bay Area Bike Share Program.</li>
</ol>

<b>Final Output Data Columns</b>

| Column Name           | dtype      | Description                                                                                                                          |
|----------------------|------------|---------------------------------------------------------------------------------------------------------------------------------------|
| `station_id`         |  object    | Number ID for the station                                                                                                             |
| `station_name`       |  object    | Name of the station                                                                                                                   |
| `lat`                |  float64   | Latitude coordinate of the station                                                                                                    |
| `long`               |  float64   | Longitude coordinate of the station                                                                                                   |
| `dock_count`         |  int64     | Number of docks at the station                                                                                                        |
| `region`             |  object    | City/service area the station is located within                                                                                       |
| `first_service_date` |  datetime  | Date that the station became active                                                                                                   |
| `last_service_date`  |  datetime  | Date that the station became inactive else the final date in the recorded data (gathered from `trips_data` last trip completion date) |
| `zip_code`           |  int64     | Zip code the station is located within                                                                                                |
| `days_in_service`    |  int64     | Days between `last_service_date` and `first_service_date`                                                                             |
| `elevation_meters`   |  float64   | Collected from polling the Google Maps Elevation API                                                                                  |
| `elevation_feet`     |  float64   | Meters converted to feet by dividing `elevation_meters` by 0.3048                                                                     |

### Dark Sky Data

<p>Dark Sky is a weather data provider and includes a Time Machine API to view historical hourly weather data.  The API is polled in another script and the output files are stored in CSV format to be cleaned</p>
<ol>
    <li>`time` is provided in unix timestamp at GMT, converted to human readable datetime localized to Pacific Standard Time</li>
    <li>`is_raining` is determined by precipitation amount being over 0.0, or if the type is reported as 'Rain'</li>
</ol>

<b>Final Output Data Columns</b>

| Column Name           | dtype      | Description                                                                                              |
|-----------------------|------------|----------------------------------------------------------------------------------------------------------|
| `apparentTemperature` |  float64   | The apparent (or “feels like”) temperature in degrees Fahrenheit.                                        |
| `cloudCover`          |  float64   | The percentage of sky occluded by clouds, between 0 and 1, inclusive.                                    |
| `daily_icon`          |  object    | A machine-readable text summary of this data point, daily                                                |
| `daily_summary`       |  object    | A human-readable summary of this data block, daily                                                       |
| `hourly_icon`         |  object    | A machine-readable text summary of this data point, hourly                                               |
| `hourly_summary`      |  object    | A human-readable summary of this data block, hourly                                                      |
| `humidity`            |  float64   | The relative humidity, between 0 and 1, inclusive.                                                       |
| `precipIntensity`     |  float64   | The intensity (in inches of liquid water per hour) of precipitation occurring at the given time.         |
| `precipProbability`   |  float64   | The probability of precipitation occurring, between 0 and 1, inclusive.                                  |
| `is_raining`          |  bool      | True if is precipitating at the time, else False                                                         |
| `temperature`         |  float64   | The air temperature in degrees Fahrenheit.                                                               |
| `time`                |  int64     | Time of weather rport localized to Pacific Standard Time, local to the bike share program                |
| `visibility`          |  float64   | The average visibility in miles, capped at 10 miles.                                                     |
| `windBearing`         |  float64   | The direction that the wind is coming from in degrees, with true north at 0° and progressing clockwise.  |
| `windSpeed`           |  float64   | The wind speed in miles per hour.                                                                        |
| `region`              |  object    | City/service area of the weather report                                                                  |

### Trip Data

<p>The trip data is in a collection of 4 files, each including records for each recorded trip taken as part of the program</p>

<ol>
    <li>Prune to include only trips within San Francisco and 180 minutes or less in duration</li>
    <li>`user_zip` is the user home zip code and from notes provided with the data set we know that these are likely to not be accurate as they were user reported.  Also this data was not collected until a few months after the program went live.</li>
    <li><ul>`additional_charges` is the value of additional charges assigned to the trip
        <li><b>Subscribers:</b> are charged $3 per 15 minute window over 45 minutes</li>
        <li><b>Customers:</b> are charged $3 per 15 minute window over 30 minutes</li>
    </ul></li>
</ol>

<b>Final Output Data Columns</b>

| Column Name           | dtype      | Description                                                                                              |
|-----------------------|------------|----------------------------------------------------------------------------------------------------------|
| `trip_id`             | int64      | Unique trip identification number                                                                        |
| `duration`            | int64      | Trip duration in seconds                                                                                 |
| `start_date`          | datetime64 | Trip start date and time                                                                                 |
| `start_station_name`  | object     | Trip start station name                                                                                  |
| `start_station_id`    | int64      | Trip start station id number                                                                             |
| `end_date`            | datetime64 | Trip end date and time                                                                                   |
| `end_station_name`    | object     | Trip end station name                                                                                    |
| `end_station_id`      | int64      | Trip end station id number                                                                               |
| `bike_id`             | int64      | Bike identification number                                                                               |
| `user_type`           | category   | User type, 'Subscriber' or 'Customer'                                                                    |
| `user_zip`            | object     | User home zip code, valid US zips only, else '00000'                                                     |
| `is_local`            | bool       | True is user home zipcode is in the service area, else False                                             |
| `user_home_city`      | object     | Name of User Home City, from zipcode                                                                     |
| `user_home_state`     | object     | Name of User Home State, 2 character Abbreviation, from zipcode                                          |
| `user_home_county`    | object     | Name of User Home County, from zipcode                                                                   |
| `duration_minutes`    | float64    | Trip duration in minutes                                                                                 |
| `billed_minutes`      | int64      | Duration minutes rounded up to nearest full minute                                                       |
| `billed_periods`      | int64      | Number of billable periods, number of 15 minutes chunks                                                  |
| `additional_charges`  | float64    | Additional Charges                                                                                       |




# Additional Information
## Authors
* **Sam Gutentag** - [www.samgutentag.com](www.samgutentag.com)

See other projects by Sam on [Github](https://github.com/samgutentag)

## Acknowledgments
* [Bay Area Bike Share](https://www.fordgobike.com) (now FordGoBike)
* [Simon Worgan](https://www.linkedin.com/in/simon-worgan-44613138/) for Mentorship and Feedback
* [DarkSky](https://darksky.net) for Historical Weather Data
* [AggData](https://www.aggdata.com/node/86) for United States Zipcode information
