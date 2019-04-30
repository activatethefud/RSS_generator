from selenium import webdriver
from bs4 import BeautifulSoup
import sys
import re

''' TODO Write documentation '''

if len(sys.argv) == 2 and sys.argv[1] == '-':
	read_from_stdin_flag=True
	stdin_lines=[]
	for stdin_line in sys.stdin.readlines():
		stdin_lines.append(stdin_line.rstrip('\n'))
else:
	read_from_stdin_flag=False

class Generator:
	def __init__(self,channel_title=None,channel_link=None,channel_description=None):
		titles=open("titles","w+")
		links=open("links","w+")
		self.archived_titles=[]
		self.archived_links=[]
		for archived_title in titles.readlines():
			self.archived_titles.append(archived_title.rstrip('\n'))
		for archived_link in links.readlines():
			self.archived_links.append(archived_link.rstrip('\n'))
		self.channel_title=channel_title
		self.channel_link=channel_link
		self.channel_description=channel_description
		options=webdriver.FirefoxOptions()
		options.add_argument("--headless")
		self.browser=webdriver.Firefox(firefox_options=options)
		self.browser.get(self.channel_link)
		self.bsObj=BeautifulSoup(self.browser.page_source,"lxml")
		links.close()
		titles.close()
	
	def find_new_articles(self):
		self.new_titles=[]
		self.new_links=[]
		self.new_descriptions=[]
		''' Edit this according to the site you are 
		    generating the RSS feed for '''
		if read_from_stdin_flag is True:
			title_selector=stdin_lines[3]
			link_selector=stdin_lines[4]
			description_selector=stdin_lines[5]
		else:
			title_selector=input("Enter the title CSS selector: ")
			link_selector=input("Enter the link CSS selector: ")
			description_selector=input("Enter description CSS selector: ")
		for title in self.browser.find_elements_by_css_selector(title_selector):
			self.new_titles.append(title.text)
		for link in self.browser.find_elements_by_css_selector(link_selector):
			self.new_links.append(link.get_attribute("href"))
		for description in self.browser.find_elements_by_css_selector(description_selector):
			self.new_descriptions.append(description.text)


	def error_no_new_articles(self):
		if len(self.new_titles) == 0 or len(self.new_links) == 0:
			print("No new articles, exiting!")
			sys.exit(2)
	
	def generate_feed_entry(self):
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
		self.browser.quit()
	
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
	if read_from_stdin_flag is True:
		title=stdin_lines[0]
		link=stdin_lines[1]
		description=stdin_lines[2]
	else:
		title=input("Enter the feed title: ")
		link=input("Enter the feed link: ")
		description=input("Enter the feed description: ")
	generator=Generator(title,link,description)
	generator.find_new_articles()
	generator.error_no_new_articles()
	generator.generate_feed_entry()
	generator.archive_new_feeds()
main()
