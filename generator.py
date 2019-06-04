from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
import os
import sys 
from random import *
from Generator import *

''' This is a simple python script that generates RSS feeds from any site.  It
uses CSS selectors to identify titles, links and article descriptions.  When
called with no argument, it asks for information like: channel title, link and
description, then it goes to ask for the CSS selectors for article title, link
and description. Scans the working directory and uses all .txt files as inputs
and makes feeds.

Stdin file format: 
Channel_Name
Channel_Link
Channel_Description (1 liner)
Article_Title_CSS_Selector
Article_Link_CSS_Selector
Article_Description_CSS_Selector

CSS Selectors can be easily copied using the browser. I've used Firefox and in
it you do: Right click (On the element you need the CSS selector for) ->
Inspect element -> Once you've identified the correct element, by right
clicking on the element, you can find Copy -> CSS Selector.

WARNING By default the browser copies the CSS selector for that particular
element, ex.:

div.listingResult:nth-child(2) > a:nth-child(1) > article:nth-child(1) >
div:nth-child(2) > header:nth-child(1) > h3:nth-child(1)

This selector will then select this particular element every time. To make it
select all of the elements with the same CSS selector, you must change the
first number to N, ex.:

2 -> n

div.listingResult:nth-child(n) > a:nth-child(1) > article:nth-child(1) >
div:nth-child(2) > header:nth-child(1) > h3:nth-child(1)

This is how it should look. When all of the arguments are set, and the program
runs, it will create the .xml feed file, with no whitespaces in the name.  '''

''' Proxy setup. This is needed in case some site blocks your IP address. 
Please be mindful and don't create too much traffic. Add a random delay between
your scans '''


# Set up Firefox preference for proxy with TOR

def setup_webdriver():
	fp=webdriver.FirefoxProfile()
	options=webdriver.FirefoxOptions()
	options.add_argument("--headless")

	# Set up proxy prefrences	
	fp.set_preference("network.proxy.type", 1)
	fp.set_preference("network.proxy.socks","127.0.0.1")
	fp.set_preference("network.proxy.socks_port",9050)
	fp.update_preferences()

	return webdriver.Firefox(firefox_profile=fp,options=options)

browser=setup_webdriver()

def main():
	''' Iterate over all .txt files in the directory.  This is useful for
	making a script that periodically scans all feeds for updates, without
	opening a new browser for each feed ''' 
	for feed in os.listdir("."):

		if feed.endswith(".txt"):

			input_file=open(feed,"r")
			information=input_file.readlines()

			''' Strip newline from every line of input '''
			i=0
			info_len=len(information)
			while i<info_len:
				information[i]=information[i].rstrip('\n')
				i+=1

			''' Grab the information to send to the generator '''
			title=information[0]
			link=information[1]
			description=information[2]

			browser.get(link)

			title_selector=information[3]
			link_selector=information[4]
			description_selector=information[5]
		
			generator=Generator(browser,title,link,description)
			generator.find_new_articles(title_selector,link_selector,description_selector)

			if generator.error_no_new_articles() is True:
				continue

			if os.path.isfile(generator.get_filename()) is False:
				generator.generate_new_feed()
			else:
				generator.append_feed()

			generator.archive_new_feeds()

			input_file.close()

	browser.quit()
main()
