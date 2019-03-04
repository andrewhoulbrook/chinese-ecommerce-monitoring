#!/usr/bin/python
# -*- encoding: utf-8 -*-
# A Maltego Transform to retrieve results from keyword search of smzdm.com
import sys
import codecs
from MaltegoTransform import *
from scraper import scrapeListings

# Initialize Maltego library
m = MaltegoTransform()

# Take keywords/phrase from a Maltego chart entity's value to search smzdm.com
keywords = (sys.argv[1]).decode('utf8')

# Call the smzdm.com scrapper. The scapper returns a JSON array of product items found matching the keyword.
items = scrapeListings(keywords)

# Loop results and output each product lising in the results as a seperate Maltego entity
if len(items) > 0:
    for item in items:
        # Return an custom smzdm.itemlisting entity to Maltego chart, with several additional information fields
        myEntity = m.addEntity('smzdm.itemlisting', item['item'].encode('utf8', errors='ignore'))
        myEntity.addAdditionalFields('item', 'Item Name', False, item['item'].encode('utf8', errors='ignore'))
        myEntity.addAdditionalFields('item-price', 'List Price', False, item['price'].encode('utf8', errors='ignore'))
        myEntity.addAdditionalFields('item-description', 'Item Description', False, item['description'].encode('utf8', errors='ignore'))
        myEntity.addAdditionalFields('item-type', 'Item Category Type', False, item['type'].encode('utf8', errors='ignore'))
        myEntity.addAdditionalFields('item-platform', 'Platform', False, item['shop'].encode('utf8', errors='ignore'))
        myEntity.addAdditionalFields('item-url', 'URL', False, item['url'].encode('utf8', errors='ignore'))
        myEntity.addAdditionalFields('url', 'Original Platform URL', False, item['source_url'].encode('utf8', errors='ignore'))
        myEntity.addAdditionalFields('item-image-url', 'Image URL', False, item['image'].encode('utf8', errors='ignore'))
        if item['image'] != 'None':
            myEntity.setIconURL(item['image'].encode('utf8', errors='ignore'))
else:
    # If no results are returned, output a Phrase entity to Maltego chart indicate null return.
    myEntity = m.addEntity('maltego.Phrase', 'No items found')

# Return entity to Maltego chart
m.returnOutput()