# MULTIJUMIA WEBSITES SCRAPER

[![python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Python](https://img.shields.io/badge/python-3.10-blue.svg)

## Presentation <br>

The Scrapy program from this repo allows the `user` to scrap data from multiple Jumia websites simultaneously by running a single command line.<br>
Data is retrieved from sites based in the following countries:
- Kenya 
- Nigeria
- Uganda
- Algeria
- Tunisia
- Morocco
- Ivory Coast
- Senegal

#### What is jumia?

Jumia is a Pan-African technology company that is built around a marketplace, logistics service and payment service. The logistics service enables the delivery of packages through a network of local partners while the payment services facilitate the payments of online transactions within Jumia’s ecosystem. It has partnered with more than 100,000 active sellers and individuals and is a direct competitor to Konga in Nigeria and Amazon in Egypt.


#### Prerequisites

- Python

versions`3.10` or `3.8`

##### Install and run

create a virtual environment

```shell
virtualenv venv
```

... activate it

```shell
source venv/bin/activate
```

- Clone the repo
- open JUMIA_INTER folder
- install dependencies 

```shell
pip install -r requirements.txt 
```
or 

```shell
pip install scrapy
```

To scrape all sites simultaneously from the root of the project run :

```shell
python run_spider.py
```

To scrape a single spider :

- from the root :

```shell
scrapy crawl <spidername> ex: jumia_kenya or jumia_senegal>
```

- from a single spider :

got to spiders folder

```shell
cd JUMIA_INTER/JUMIA_INTER/spiders
```
choose your spider and run it :

```shell
scrapy runspider jumia_kenya.py 
``` 











