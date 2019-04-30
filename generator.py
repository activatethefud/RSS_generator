from selenium import webdriver
from bs4 import BeautifulSoup
import sys
import re

''' TODO Write documentation '''

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
		self.browser.quit()
		links.close()
		titles.close()
	
	def find_new_articles(self):
		self.new_titles=[]
		self.new_links=[]
		self.new_descriptions=[]
		''' Edit this according to the site you are 
		    generating the RSS feed for '''
		for new_article in self.bsObj.findAll("article",{"class":"item-list"}):
			new_title=new_article.find("h2").get_text()
			new_link=new_article.find("h2").find("a")["href"]
			new_description=new_article.find("div",{"class":"entry"}).find("p").get_text()
			if new_title not in self.archived_titles and new_link not in self.archived_links:
				self.new_titles.append(new_title)
				self.new_links.append(new_link)
				self.new_descriptions.append(new_description)	

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
	generator=Generator("DanUBeogradu","https://www.danubeogradu.rs/rubrike/izlasci/","Desavanja u Beogradu")
	generator.find_new_articles()
	generator.error_no_new_articles()
	generator.generate_feed_entry()
	generator.archive_new_feeds()
main()
