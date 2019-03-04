#!/usr/bin/python
# -*- encoding: utf-8 -*-
# Extract list price from smzdm.com item listing
import sys
import codecs
from MaltegoTransform import *

# Initialize Maltego library
m = MaltegoTransform()

# Extract the listed price from the Maltego smzdm item entity
m.parseArguments(sys.argv)
price = m.getVar('item-price').decode('utf8')

# Add entity to the Maltego chart
myEntity = m.addEntity('smzdm.itemprice', price.encode('utf8', errors='ignore'))

# Return entity to Maltego
m.returnOutput()
