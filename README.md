# ASO-collector

## Requirements:
- Python 3.6 or up installed 
- Update apt-get ```sudo apt-get update```
- Python developer package ```sudo apt install python3.6-dev build-essential```
- virtualenv ```sudo apt install virtualenv```
- NodeJs installed ```sudo apt install nodejs npm```
- awscli ```sudo apt install awscli```


## Setup:
- clone repository
- ```cd ASO-collector```
- ```. install.sh```
- Create service account in GCP console and give it required permission to access bucket containing Play Store reports. Download .json file with account credentials and place it on same machine as this project. More info on how to configure it: https://support.google.com/googleplay/android-developer/answer/6135870?hl=en
- Fill .env with all env variables from .env.example (env variable description below)
- Create service account for accessing AWS bucket and run ```asw configure```.
- Download Search Ads certificates and set SEARCH_ADS_CERTIFICATES env.


## Env variables:
- ```GOOGLE_APPLICATION_CREDENTIALS=``` path to .json file with Google service account credentials for accessing acquisition reports. 
- ```GCP_PLAY_STORE_REPORTS_BUCKET_NAME=``` Google Play Store bucket name where acquisition reports are stored.
- ```SEARCH_ADS_CERTIFICATES=``` path to directory with Search Ads certificates. Files should have names: search-ads.key, search-ads.pem
- ```AWS_S3_BUCKET_NAME=``` AWS bucket name where data exports will be stored.
- ```DEFAULT_EXPORT_FROM=``` Date (format 'YYYY-MM-DD') from which script will try get data exports.
- ```FEATURED_TODAY_APP_NAME=``` String that should be contained in app title while getting featured today export. 
- ```ASO_SEARCH_TERM=``` Term for 10 first apps data export.


## Usage:

Run ```python exporter/main.py``` inside virtualenv to retrieve data from between DEFAULT_EXPORT_FROM and todays date minus three days. Date from which export takes place is optimized based on exported_data content. Script check what is last date inside corresponding .csv file. To disable this option set OPTIMIZE_EXPORT_FROM=0.

To run for specific period ```OPTIMIZE_EXPORT_FROM=0 python exporter/main.py 2019-10-10 2019-10-30``` where first date is from when export should take place and second argument is end date.

Script after running command will perform following actions:
1. Download all exports files from AWS bucket.
2. Optimize export from date based on content of exported_data directory for each export.
3. Call all endpoints to get requested data.
4. Process data and create aggregated on daily, weekly and monthly bases export files.
5. Store files in AWS bucket

To run export only for specific data source run script file from module e.g. ```python exporter/app_follow/script.py```


Known issues:
- Apps Flyer return 416 error (probably credentail issue)
- App Store export takes very long time to finish (can do request every 10 sec for one data point, there is 10 per country for date). 
- SensorTower return 500 for big amounts of data (e.g.)

## Additional commands:
- ```python setup.py clear_old_logs``` will delete logs files older by default than 7 days.
- ```python setup.py remove_raw_data``` will delete all raw data stored in raw_data directory.


# ASO-collector Dashboard


## Description:

React application that display data collected by ASO-collector scripts on various charts and tables. It require read access to bucket where export file are store. 


## Requirements:
- NodeJs installed 


## Setup:
- clone repository
- ```cd ASO-collector/frontend```
- ```npm install```
- set PUBLIC_URL in .env.production to domain where app will be served (e.g. S3 bucket URL, do it before building app and deploying)
- ```npm run build``` or ```npm start``` for development.
- deploy as any single page application (it is highly recommended to configure HTTPS as not to pass AWS service account credentials without encryption).


## Usage:
- On login page provide AWS bucket name where export data are stored, AWS access key id and
AWS secret access key of service account (best with only read access).
- Requested data are cached for 1 hour in browser to lower amount of requests.



## Stories short summary:
- ASO-1 - Init project
- ASO-2 - Google Play export
- ASO-3 - Ratings export
- ASO-4 - Reviews export 
- ASO-5 - Ranking export
- ASO-6 - App Store export 
- ASO-7 - Apps Flyers Export
- ASO-8 - Data upload
- ASO-9 - Dashboard
- ASO-10 - Export script interface
- ASO-11 - Feature export
- ASO-12 - Versions export
- ASO-13 - Keywords export
- ASO-14 - Keywords export app follow
- ASO-15 - Prepare final data export
