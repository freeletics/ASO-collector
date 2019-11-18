#!/bin/bash
echo 'install python app'
virtualenv -p python3 env
. env/bin/activate
pip install -e .
pip install -r requirements.txt

echo 'install node app'
cd exporter/app_store_node
npm i
cd ../..

echo 'create data directories'
mkdir logs
mkdir raw_data
mkdir exported_data

echo 'create empty .env file'
touch .env
