#!/usr/bin/python
# -*- encoding: utf-8 -*-
# Extract platform from smzdm.com item listing
import sys
import codecs
from MaltegoTransform import *

# Initialize Maltego library
m = MaltegoTransform()

# Extract the platfrom name from the Maltego smzdm item entity
m.parseArguments(sys.argv)
platform = m.getVar('item-platform').decode('utf8')

# Add entity to the Maltego chart
myEntity = m.addEntity('smzdm.itemplatform', platform.encode('utf8', errors='ignore'))

# Return entity to Maltego
m.returnOutput()
