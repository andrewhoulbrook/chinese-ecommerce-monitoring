#!/usr/bin/python
# -*- encoding: utf-8 -*-
# Extract product category from smzdm.com item listing
import sys
import codecs
from MaltegoTransform import *

# Initialize Maltego library
m = MaltegoTransform()

# Extract the item categorisation from the Maltego smzdm item entity
m.parseArguments(sys.argv)
category = m.getVar('item-type').decode('utf8')

# Add entity to the Maltego chart
myEntity = m.addEntity('smzdm.itemcategory', category.encode('utf8', errors='ignore'))

# Return entity to Maltego
m.returnOutput()
