#!/usr/bin/python
# -*- encoding: utf-8 -*-
# View original product listing (on original platform) found via smzdm.com search results
# Launches a browser via Selenium with the URL of the original product listing. 
import sys
import codecs
from MaltegoTransform import *
from selenium import webdriver

# Local path to Webdriver (e.g. chromedriver or geckodriver) for Selenium
FIREFOX_PATH = 'geckodriver.exe'
#CHROME_PATH = './chromedriver.exe'

# Initialize Maltego library
m = MaltegoTransform()

# Handle input string (a URL) passed from Maltego chart entity 
m.parseArguments(sys.argv)
item_url = m.getVar('url').encode('utf8', errors='ignore')

if item_url:

    # Initialize a Selenium brower object with the URL
    try:
        browser = webdriver.Firefox(FIREFOX_PATH)
        # browser = webdriver.Chrome(CHROME_PATH)
        browser.set_page_load_timeout(5)
        browser.get(item_url)
    except Exception as e:
        # Pass error message to Maltego UI
        m.addUIMessage('{}: {}'.format("Selenium/Webdriver error: ",e))
else:
    # Pass error message to Maltego UI
    m.addUIMessage("No URL provided.")

# Return entity to Maltego chart
m.returnOutput()
