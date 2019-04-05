# Baseball Statistics Scraper Installation Guide

## Retrieve code

* `$ https://github.com/realchief/Scrapy-baseball-statistics.git`

## Create Vritual Environment

* `$ sudo apt-get install python-virtualenv`
* `$ cd baseballstatistics`
* `$ virtualenv venv`
* `$ source venv/bin/activate`


## Install packages

* `$ pip install -r requirements.txt`


## Run spiders

* `$ cd baseballstatistics/spiders`
* `$ scrapy crawl scrapingdata -o result2017.json`

## Check result2017.json
