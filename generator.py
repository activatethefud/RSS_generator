from selenium import webdriver
import os
import sys

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

# Set webdriver as global
options=webdriver.FirefoxOptions()
#options.add_argument("--headless")
browser=webdriver.Firefox(options=options)


class Generator:
	def __init__(self,channel_title=None,channel_link=None,channel_description=None):
		''' This sets up the generator. The archived article titles and
		links are read into memory. If no "titles" and "links" files
		are present, they will be created. The channel title, link, and
		description is set. The browser opens and waits for the
		javascript to execute, and load the newly made html. '''

		titles=open("titles","r")
		links=open("links","r")

		self.archived_titles=[]
		self.archived_links=[]
		self.channel_link=channel_link
		self.channel_title=channel_title
		self.channel_description=channel_description

		for archived_title in titles.readlines():
			self.archived_titles.append(archived_title.rstrip('\n'))

		for archived_link in links.readlines():
			self.channel_description=channel_description


		links.close()
		titles.close()
	
	def find_new_articles(self,title_selector,link_selector,description_selector):
		''' This is the bread and butter. This function is the one that
		extracts the article info from the site. Some sites provide the
		description in two paragraph elements for whatever reason. If
		this is the case, I encourage you to edit the code yourself, or
		wait for the feature to get coded, lmao. '''

		self.new_titles=[]
		self.new_links=[]
		self.new_descriptions=[]
		
		for title in browser.find_elements_by_css_selector(title_selector):
			if title.text not in self.archived_titles:
				self.new_titles.append(title.text)

		for link in browser.find_elements_by_css_selector(link_selector):
			if link.get_attribute("href") not in self.archived_links:
				self.new_links.append(link.get_attribute("href"))

		for description in browser.find_elements_by_css_selector(description_selector):
			self.new_descriptions.append(description.text)


	def error_no_new_articles(self):
		''' Check if any new information is found, if not. Exit and
		inform the user. '''

		if len(self.new_titles) == 0 or len(self.new_links) == 0:

			print("No new articles, exiting!")

			browser.quit()
			sys.exit(2)
	
	def generate_feed_entry(self):
		''' This just does the work of actually writing the .xml file
		with the extracted information. Nothing spectacular. '''

		entry=open(self.channel_title.replace(" ","") + ".xml","w")
		entry.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
		entry.write('<rss version="2.0">\n')
		entry.write("<channel>\n")
		entry.write("  <title>" + self.channel_title + "</title>\n")
		entry.write("  <link>" + self.channel_link + "</link>\n")
		entry.write("  <description>" + self.channel_description + "</description>\n")

		i=0
		num_of_entries=len(self.new_titles)

		while i<num_of_entries:
			entry.write("  <item>\n")
			entry.write("    <title>" + self.new_titles[i] + "</title>\n")
			entry.write("    <link>" + self.new_links[i] + "</link>\n")
			entry.write("    <description>" + self.new_descriptions[i] + "</description>\n")
			entry.write("  </item>\n")
			i+=1
		entry.write("</channel>\n")
		entry.write("</rss>")

	def archive_new_feeds(self):

		links=open("links","a")
		titles=open("titles","a")

		for link in self.new_links:
			links.write(link + '\n')

		for title in self.new_titles:
			titles.write(title + '\n')

		links.close()
		titles.close()

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
		
			generator=Generator(title,link,description)
			generator.find_new_articles(title_selector,link_selector,description_selector)
			generator.error_no_new_articles()
			generator.generate_feed_entry()
			generator.archive_new_feeds()

			input_file.close()

	browser.quit()
main()

