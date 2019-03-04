#!/usr/bin/python
# -*- encoding: utf-8 -*-
# The main logic of the smzdm.com Web scraper
import requests, time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime

# Initialize a new User Agent, used to generate random HTML headers for GET requests. 
ua = UserAgent()

# Check for more pages of item listings
def pagenation(page):
    pagenation_block = page.find('div', {'class':'feed-pagenation'})
    if pagenation_block:
        page_refs = pagenation_block.find_all('a', href=True)
        if u'下一页' in page_refs[len(page_refs)-1].text:
            return True
        else:
            return False
    else:
        return False

# Scrape out the main items of data from each item listing
def scrapeItem(item):
    title_block = item.find('h5')
    desc_block = item.find('div', {'class':'feed-block-descripe'})
    footer_block = item.find('span', {'class':'feed-block-extras'})
    source_button = item.find('div', {'class':'feed-link-btn'})
    image_ref = item.find('img')
    url = scrapeURL(title_block)
    item_type, scrape_date = scrapeProductDetails(url)
    data = {
	'item':' '.join(title_block.text.split()).strip(),
	'price':scrapePrice(title_block),
	'url':url,
    'date':scrape_date,
    'source_url':scrapeSourceURL(source_button),
	'description':' '.join(desc_block.text.split()).strip()
,	'image':scrapeImage(image_ref),
	'shop':scrapeShop(footer_block),
    'type':item_type}
    return data

# Scrape out the URL for a specific item listing in smzdm.com
def scrapeURL(title_block):
    item_ref = title_block.find('a', href=True)
    item_url = item_ref['href'].strip()
    return item_url

# Scrape out the URL for the original item listing collated by smzdm.com
def scrapeSourceURL(source_button):
    if source_button:
        source_ref = source_button.find('a', href=True)
        source_url = source_ref['href'].strip()
    else:
        source_url = 'None'
    return source_url

# Scrape out the advertised price in the item listing
def scrapePrice(title_block):
    price_block = title_block.find('div', {'class':'z-highlight'})
    if price_block:
        price = ' '.join(price_block.text.split()).strip()
    else:
        price = 'None Found'
    return price

# Scrape out the name of the original e-Commerce platform where the item was listed
def scrapeShop(footer_block):
    shop_span = footer_block.find('span')
    if shop_span:
        shop = ' '.join(shop_span.text.split()).strip()
    else:
        shop = 'None'
    return shop

# Scrape out the URL for the image associated with item listing in smzdm.com
def scrapeImage(image_ref):
    if image_ref:
        image_url = 'http:' + image_ref['src'].strip()
    else:
        image_url = 'None'
    return image_url

# Get the dedicated page for the item listing in smzdm.com, scrape out details about the what type of item it is
def scrapeProductDetails(item_url):
    dets_HTML = requests.get(item_url, headers={'user-agent': ua.random})
    dets_soup = BeautifulSoup(dets_HTML.content, 'lxml')
    crumbs = dets_soup.find_all('div', {'class':'crumbsCate'})
    if crumbs:
        item_type = crumbs[len(crumbs)-1].text.strip()
    else:
        item_type = 'None'
    meta_data = dets_soup.find('div', {'class':'article-meta-tip'})
    if meta_data:
        date_pattern = re.match(r'[0-9][0-9]-[0-9][0-9]', meta_data.text)
        scrape_date = str(datetime.now().year) + date_pattern.group(1)
    else:
        scrape_date = 'None'
    return item_type, scrape_date

# Build the search URL and header, search for items related to keywords via smzdm.com
def scrapeListings(keywords):
    scrapped_items = []

    next_page = True
    page_count = 1

    # Encode the keywords string to make it URL-safe
    keywords = '+'.join(keywords.split()).strip()

    while next_page and page_count < 11:

        url = 'http://search.smzdm.com/?c=home&s={}&v=b&p={}'.format(keywords, page_count)
        print url
        page_HTML = requests.get(url, headers={'user-agent': ua.random})
        page_soup = BeautifulSoup(page_HTML.content, 'lxml')
        item_feed = page_soup.find(id='feed-main-list')
        if item_feed:
            items = item_feed.find_all('li')
            for item in items:
                item_data = scrapeItem(item)
                scrapped_items.append(item_data)

        next_page = pagenation(page_soup)
        page_count += 1
        time.sleep(2)

    return scrapped_items
