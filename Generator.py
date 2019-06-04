from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
import os
import sys 
from random import *

# Helper function needed to turn & intp &amp
def format_title_special_chars(title):
	return title.replace("&","&amp")


class Generator:
	def __init__(self,browser=None,channel_title=None,channel_link=None,channel_description=None):
		''' This sets up the generator. The archived article titles and
		links are read into memory. If no "titles" and "links" files
		are present, they will be created. The channel title, link, and
		description is set. The browser opens and waits for the
		javascript to execute, and load the newly made html. '''

		# Create titles and links if they don't exist.
		if os.path.isfile("titles") is False:
			open("titles","w").close()
		if os.path.isfile("links") is False:
			open("links","w").close()

		titles=open("titles","r")
		links=open("links","r")

		self.browser=browser
		self.archived_titles=[]
		self.archived_links=[]
		self.channel_link=channel_link
		self.channel_title=channel_title
		self.channel_description=channel_description
		self.filename=self.channel_title.replace(" ","") + ".xml"

		for archived_title in titles.readlines():
			self.archived_titles.append(archived_title.rstrip('\n'))

		for archived_link in links.readlines():
			self.channel_description=channel_description


		links.close()
		titles.close()

	def get_filename(self):
		return self.filename
	
	def find_new_articles(self,title_selector,link_selector,description_selector):
		''' This is the bread and butter. This function is the one that
		extracts the article info from the site. Some sites provide the
		description in two paragraph elements for whatever reason. If
		this is the case, I encourage you to edit the code yourself, or
		wait for the feature to get coded, lmao. '''

		self.new_titles=[]
		self.new_links=[]
		self.new_descriptions=[]
		
		for title in self.browser.find_elements_by_css_selector(title_selector):
			new_title=format_title_special_chars(title.text)
			if new_title not in self.archived_titles:
				self.new_titles.append(new_title)

		for link in self.browser.find_elements_by_css_selector(link_selector):
			if link.get_attribute("href") not in self.archived_links:
				self.new_links.append(link.get_attribute("href"))

		for description in self.browser.find_elements_by_css_selector(description_selector):
			self.new_descriptions.append(description.text)


	def error_no_new_articles(self):
		''' Check if any new information is found, if not. Exit and
		inform the user. '''

		if len(self.new_titles) == 0 or len(self.new_links) == 0:

			print("No new articles for feed %s, exiting!" % (self.channel_title))

			return 1
		return 0

	def append_feed(self):
		''' Append to the .xml file if it already exists,
		stacking entries into the feed. '''

		# Save all of the previous entries
		entry=open(self.filename,"r")
		old_entry=entry.readlines()
		entry.close()

		entry=open(self.filename,"w")

		# Delete closing tabs to prepare for appending
		del old_entry[-1]
		del old_entry[-1]

		for line in old_entry:
			entry.write(line)

		# Append new feeds
		i=0
		num_of_entries=len(self.new_titles)

		while i<num_of_entries:
			entry.write("  <item>\n")
			entry.write("    <title>" + self.new_titles[i] + "</title>\n")
			entry.write("    <link>" + self.new_links[i] + "</link>\n")
			entry.write("    <description>" + self.new_descriptions[i] + "</description>\n")
			entry.write("  </item>\n")
			i+=1
		
		# Close the feed
		entry.write("</channel>\n")
		entry.write("</rss>")
		entry.close()
			
	def generate_new_feed(self):
		''' Generate the starting .xml file to later append new feeds to '''

		entry=open(self.filename,"w")
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
		entry.close()

	def archive_new_feeds(self):

		links=open("links","a")
		titles=open("titles","a")

		for link in self.new_links:
			links.write(link + '\n')

		for title in self.new_titles:
			titles.write(title + '\n')

		links.close()
		titles.close()
