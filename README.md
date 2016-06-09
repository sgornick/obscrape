# obscrape

Example of how to scrape an e-commerce site for product items, then add those items to an OpenBazaar store.

This crawler will be specific to the e-commerce site.

This is published for educational purposes only.  The crawler is filtered to pull only 30 items.

This is a one-way push to OpenBazaar.  There is no synching. Running the obpush script a second time will cause duplicate listings.

## Installation

``` sh
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

```

## Usage

To scrape the data from the e-commerce site:

``` sh

$ scrapy crawl lvr-crawler -o data/items.json

```

To add those items to the OpenBazaar store:

``` sh

$ python obpush.py

```
