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

<ol>The stations data is in a collection of 4 files, each including the status of all stations that are active at the time the data was collected.  Additionally, Bay Area Bike Share published a `README.txt` file with each data set that includes notes on station expansion and relocation dates.
    <il>For each station, drop duplicated rows, reported when a station does not move or change between data collection times.</li>
    <il>Next we attend to each note included in the `README` files</li>
</ol>

<b>Final Output Data Columns</b>

| Column Name           | dtype      | Description                                                                                                                          |
|----------------------|------------|---------------------------------------------------------------------------------------------------------------------------------------|
| `station_id`         | (object)   | number ID for the station                                                                                                             |
| `station_name`       | (object)   | name of the station                                                                                                                   |
| `lat`                | (float64)  | latitude coordinate of the station                                                                                                    |
| `long`               | (float64)  | longitude coordinate of the station                                                                                                   |
| `dock_count`         | (int64)    | number of docks at the station                                                                                                        |
| `region`             | (object)   | city/service area the station is located within                                                                                       |
| `first_service_date` | (datetime) | date that the station became active                                                                                                   |
| `last_service_date`  | (datetime) | date that the station became inactive else the final date in the recorded data (gathered from `trips_data` last trip completion date) |
| `zip_code`           | (int64)    | zip code the station is located within                                                                                                |
| `days_in_service`    | (int64)    | `last_service_date` - `first_service_date`                                                                                            |
| `elevation_meters`   | (float64)  | collected from polling the Google Maps Elevation API                                                                                  |
| `elevation_feet`     | (float64)  | meters converted to feet by dividing `elevation_meters` by 0.3048                                                                     |

### Dark Sky Data

<ol>Dark Sky is a weather data provider and includes a Time Machine API to view historical hourly weather data.  The API is polled in another script and the output files are stored in CSV format to be cleaned
    <il>`time` is provided in unix timestamp at GMT, converted to human readable datetime localized to Pacific Standard Time</li>
    <il>`is_raining` is determined by precipitation amount being over 0.0, or if the type is reported as 'Rain'</li>
</ol>

<b>Final Output Data Columns</b>

| Column Name           | dtype      | Description                                                                                              |
|-----------------------|------------|----------------------------------------------------------------------------------------------------------|
| `apparentTemperature` | (float64)  | The apparent (or “feels like”) temperature in degrees Fahrenheit.                                        |
| `cloudCover`          | (float64)  | The percentage of sky occluded by clouds, between 0 and 1, inclusive.                                    |
| `daily_icon`          | (object)   | A machine-readable text summary of this data point, daily                                                |
| `daily_summary`       | (object)   | A human-readable summary of this data block, daily                                                       |
| `hourly_icon`         | (object)   | A machine-readable text summary of this data point, hourly                                               |
| `hourly_summary`      | (object)   | A human-readable summary of this data block, hourly                                                      |
| `humidity`            | (float64)  | The relative humidity, between 0 and 1, inclusive.                                                       |
| `precipIntensity`     | (float64)  | The intensity (in inches of liquid water per hour) of precipitation occurring at the given time.         |
| `precipProbability`   | (float64)  | The probability of precipitation occurring, between 0 and 1, inclusive.                                  |
| `is_raining`          | (bool)     | True if is precipitating at the time, else False                                                         |
| `temperature`         | (float64)  | The air temperature in degrees Fahrenheit.                                                               |
| `time`                | (int64)    | Time of weather rport localized to Pacific Standard Time, local to the bike share program                |
| `visibility`          | (float64)  | The average visibility in miles, capped at 10 miles.                                                     |
| `windBearing`         | (float64)  | The direction that the wind is coming from in degrees, with true north at 0° and progressing clockwise.  |
| `windSpeed`           | (float64)  | The wind speed in miles per hour.                                                                        |
| `region`              | (object)   | city/service area of the weather report                                                                  |

### Trip Data





# Additional Information
## Authors
* **Sam Gutentag** - *Initial work* - [samgutentag](www.samgutentag.com)

See other projects by Sam on [Github](https://github.com/samgutentag)

## Acknowledgments
* The [Yelp Open Data Set](https://www.yelp.com/dataset)
* [Simon Worgan](https://www.linkedin.com/in/simon-worgan-44613138/)
* [Springboard](www.springboard.com)


#datascience #github
#datascience
