# China E-commerce Monitoring Workflow

A Web scrapper for [smzdm.com](https://www.smzdm.com), a Chinese e-commerce aggregator site. This repo also includes Maltego transforms that allow for the scraper to be run from the Maltego environment where the results of the scraper can be visualised and analysed further.

## Background

This was a toy project to assist colleagues working in brand protection in China. The idea was to build a workflow to enable a quick and approximate way to monitor and analyse e-commerce product listings that doesn't break the bank. The workflow aims to help analysts organise a simple workflow and monitor brands and products across different e-commerce platforms. 

It's possible to have a workflow such as this up and running in a couple hours.

Ideally, with more time invested, I'd write customized Web scrapers, or utilize any open APIs, for each e-commerce platform I'm interested in monitoring. Creating scrapers for each and every e-commerce platform in China cannot be described as a *quick solution* though. 

This workflow makes use of the free e-commerce aggregator site [smzdm.com](https://www.smzdm.com) and scrapes data directly from the site. The site already attempts to collate products listed across a range of key platforms in China.

<p align="center">
  <img src="/doc/smzdm.png">
</p>

## Designing a Monitoring and Analysis Workflow on a Budget

The workflow will consist of two halves:

* A smzdm.com Web scraper returning product listings identified via keyword search;
* A way to visualize and analyse the results returned from the Web scraper.

The Web scraper could be programmed to return results in the form of a CSV file. Something as simple as MS Excel can then be used for visualization and analysis.

## Maltego - Visual Link Analysis Tool

I've chosen to experiment with [Maltego](https://www.paterva.com/web7/buy/maltego-clients.php), more commonly a tool used in the Cyber Security industry. This will act as my front-end which I'll use to visually explore and analyse the product listings once collated.

The Python script for the Web scraper will be packaged into a *Local Transform* in Maltego. Transforms are a great feature and allow Maltego to be customized to tasks such as this one.

Building this workflow around Maltego transforms also means the user doesn't need to be familiar with Python, run Python code from the command line or involve me having to build a front-end. It's as simple as choosing 'run' from a right-click menu in a Maltego chart.

If you just want to experiment like me, you can download a free copy of Maltego Community Edition (CE). This allows you to get a look and feel but functionality will be restricted. If you like what you see, you can purchase Maltgeo and unlock all the magic.

## Prerequisites

The scraper and Maltego local transforms are all written in Python 2.7.

The following Python modules are required if you don't already have them installed:

```
import requests
import BeautifulSoup4
import UserAgent
```

and

```
import MaltegoTransform
```

This last module import is the Maltego python transform library. You can grab a copy from the [Maltego developer site](https://docs.maltego.com/helpdesk/attachments/2015007304961). 

## Installing

Required Python modules can be installed via PyPI:

```
pip install BeautifulSoup4
pip install useragent
pip install requests
```

A copy of Maltego can be [downloaded](https://www.paterva.com) for free (CE Edition) or a Pro version purchased. 

Configure the local transforms in Maltego, [see the Configuration Guide](https://docs.maltego.com/support/solutions/articles/15000010781-local-transforms). In short, you'll need to link the transforms to specific entity types and point Maltego to both your local Python installation and your local copy of these transform scripts. 

### Custom Entities for Maltego

These *smzdm transforms* can be run like any other local transform in Maltego. However, the transform will return results as a custom entity type named ```smzdm.itemlisting```. You can install my custom entities via the .mtz (and the Maltego *Import Entities* function) in the entities directory, create your own custom entities or recode to one of the standard Maltego entity types.

I linked the ```search.py``` transform to a ```maltego.Phrase``` entity. The following set of transforms should then be linked to the ```smzdm.itemlisting``` entity.

* extract_price.py
* extract_platform.py
* extract_category.py

The ```view_itemlisting.py``` script just offers the option to quickly launch a Web browser to view a product's original listing by loading the item's source URL. The transform lets me do this with a single menu click from inside Maltgeo. *Note:* this script requires additionally installing Selenium and a Web driver such as Chromedriver or Geckodriver. 

## Getting Start - MLB Example

Here's an example using a well-known brand and product, Major League Baseball (MLB) caps. Using Maltego CE, output is restricted to only the first twelve results returned by the Web scraper. That's fine for now, it keeps this example simple.

Below is the result of the simple keyword query "MLB" on smzdm.com, run inside Maltego. The search has mainly returned baseball caps, other non-cap items can be pruned from the chart. Embedded within each entity on the chart is a range of information (date, price, platform, product type, URLs, etc...) that has also been collated by the scraper.

![Example of scraper and transforms in action](/doc/mlb1.gif)

Additional transforms I've written allow for key attributes within the data to be separately extracted onto the Maltego chart to facilitate further analysis.
Price is still a highly effective indicator of the risk of counterfeit products. Below I'm running a transform to extract the price of each baseball cap as a separate entity on the chart.

![Example of scraper and transforms in action](/doc/mlb2.gif)

Two of these caps (47' Brand, New York Mets) are slightly cheaper. Focusing on these two items, I can run a similar transform to extract the name of the e-commerce platform the items were originally listed on. The platform itself another key risk indicator. Both items in this example were listed on Amazon China.

Extracting the price as a separate entity on the chart is also one way of tracking price changes as research is repeated over time. With a minor change to the Maltego transform code, the datetime-stamp can also be incorporated alongside the price.

In the background, the original Maltego transform (running the Web scraper) has extracted and structured other data in addition to price and platform. Clicking into a product entity on the Maltego chart gives me a structured view of all the collated data linked to that product.

![Example of scraper and transforms in action](/doc/mlb3.gif)

Following these two baseball caps through to the original listings on Amazon China shows that the current list price is no longer RMB 89. It has returned closer to the expected retail price. In this instance, these items were listed on a timed discount via an official MLB vendor on Amazon.

You can start to see how this can be used in a brand monitoring context and also how it can be scaled to quickly mine through much larger volumes of product listings to identify counterfeit risk patterns.

## Getting Started - Dyson Example

Here's another example with a popular imported product in China, the Dyson Supersonic Hairdryer. I've run the query "DYSON+SUPERSONIC" and kept the first seven relevant product listings on my Maltego chart shown below.

![Example of scraper and transforms in action](/doc/dyson.gif)

Extracting the prices, it's clear most listings are within a similar price bracket. Extracting the platforms, I can see some of these are products listed on Dyson's official flagship stores or sold via the platforms themselves. This gives me an indication of expected retail price.

I highlight three product listings that are priced below the expected retail price. These are associated with two specific stores, neither of which are official flagship stores. One of the stores appears to be operated by a Hong Kong trading company. This is one kind of potential risk pattern we can research further, especially if the company is not already known to us as an authorised dealer/distributor of a particular brand. 

Lower cost counterfeits from the mainland masquerading as foreign imports (often complete with fraudulent import documents) is one particular risk pattern we can examine further in this way. 

*Disclaimer: casting no accusations against this particular Hong Kong trading company, it's used here purely to illustrate to the workflow in action and how it can be used.*

## Making use of Maltego as your Investigation Environment

As well as running semi-automated transforms in Maltego, entities can be added to the chart manually. In this way, we can continue to research the operators of the two stores highlighted in the example above selling Dyson hairdryers. We can add our findings to the chart manually, building-up an wider intelligence picture and identifying potential cross-platform links.

The convenience of the Maltego environment is that the results from e-commerce monitoring can dovetail directly into any transforms built for further investigative research of registered corporate entities, individuals, user names, contact details, trade names, blacklists etc...

I also use a set a transforms built around Baidu's Fanyi API for machine translation. These allow me to switch between Chinese, Pinyin and English search terms, all within Maltego.

## Other Info

I began collecting a list of ```mall_id``` strings used by smzdm.com to reference specific platforms it aggregates. This list can be found in ```/extras/smzdm_mall_ids.json```. The list is likely incomplete and was not integrated in to ```scaper.py``` but might be of use for further development.  

If interested in building a budget workflow with reach beyond the Chinese market, you can also consider tapping into [Webhose.io's](https://webhose.io) machine-readable feed of global e-commerce data. The data comes structured and won't require relying on any temperamental Web scrapers. Webhose also retains an archive of historic pricing data that can be queried.

## Built With

* [Python](http://www.python.org)
* [BeautifulSoup's HTML Parser](https://www.crummy.com/software/BeautifulSoup/)
* [Maltego Local Python Library](https://docs.maltego.com/support/solutions/articles/15000019558-python-local-library-reference)

## Authors

* **Andrew Houlbrook** - *Initial work* - [ba2baha3o](https://github.com/ba2baha3o)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
