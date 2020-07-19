import feedparser

class Parser:
	def __init__(self, url):
		self.url = url

	def get_feed(self):
		return feedparser.parse(self.url)