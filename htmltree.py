import sys, re
import urllib
import urllib.request as req
from html.parser import HTMLParser

class HTMLNode():
	def __init__(self,tag,attrs=None):
		self.tag = tag
		self.attrs = attrs
		self.data = ""

	def write_data(self,data):
		self.data = data

	def print(self):
		print("tag: " + self.tag)
		if self.attrs:
			for attr in self.attrs:
				print("  " + attr[0] + ": " + attr[1])
		if len(self.data) > 0:
			print("data: " + self.data)

class HTMLTree():
	def __init__(self,node,parent=None):
		self.node = node
		self.parent = parent
		self.children = []

	def add_child(self,node):
		child = HTMLTree(node,self)
		self.children.append(child)
		return child

	def parent(self):
		return self.parent

	def find(self, tag, attrs=None):
		matches = []
		if self.node.tag == tag:
			matched = True
			if attrs:
				for attr in attrs:
					if attr not in self.node.attrs:
						matched = False
			if matched:
				matches = [self]
		for child in self.children:
			matches += child.find(tag,attrs)
		return matches

	def print(self):
		self.node.print()
		for child in self.children:
			child.print()

class MyHTMLParser(HTMLParser):

	def __init__(self):
		self.voidtags = ['area','base','br','col','command','embed','hr','img','input','keygen','link','param','source','track','wbr']
		root = HTMLNode("document")
		self.tree = HTMLTree(root)
		self.parent = self.tree
		super(MyHTMLParser,self).__init__()

	def handle_starttag(self, tag, attrs):
		node = HTMLNode(tag,attrs)
		child = self.parent.add_child(node)
		if tag not in self.voidtags:
			self.parent = child

	def handle_endtag(self, tag):
		self.parent = self.parent.parent

	def handle_data(self,data):
		self.parent.node.write_data(data)

	def tree(self):
		return self.tree

def parse_site(url):
	try:
		parser = MyHTMLParser()
		response = req.urlopen(url)

	except urllib.error.URLError as e:
		print(" URL error")
		print(e.reason)
		sys.exit()
	except:
		e = sys.exc_info()[0]
		print(" Error:")
		print(e)
		sys.exit()

	html = response.read().decode("utf-8")
	parser.feed(html)
	return parser

