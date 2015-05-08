# -*- coding: utf-8 -*-
from sys import argv
from bs4 import BeautifulSoup
import re
import md5

import codecs

import ipdb

script, inputf = argv

#fileh = codecs.open(inputf, "r", "utf-8","strict")
fileh = open(inputf, "r")
soup = BeautifulSoup(fileh.read())

def rmDbQ(str):
	return re.sub('"','\'',str)
def formatDate(str):
	return str[0] +" "+ str[1] + " "+ str[2] +" "+ str[3] + " "+str[4]

def getTitle(soup):
	titles = soup.find_all('a', 'titles')
	return rmDbQ(titles[0].string)

def getAuthors(soup):
    for author in soup.find_all('div', attrs = { 'class' : 'postauthor'}) :
        yield author.string

def getDates(soup):
    for date in soup.find_all('td', attrs={'class': "postbottom", "align": "center"}):
        yield date.string

def getPost(soup):
	posts = soup.find_all("div","postbody")
	prev_parent = ""
	for post in posts:
		pstr = str(post.parent)
		p = post.parent
		m = md5.new()
		m.update(pstr)
		current_parent = m.digest()
		if(current_parent!=prev_parent):
			txt = ""
			for string in p.stripped_strings:
				txt = txt + string
			yield rmDbQ(txt)
		prev_parent = current_parent


##############################3

title = getTitle(soup)
authors = getAuthors(soup)
dates = getDates(soup)
posty = getPost(soup)

forum, thread = inputf.split("_")[1:3]

#for i in range(len(posty)):
#	print unicode(forum +u";"+thread +u";\""+title + u"\";" + authors[i] + u";" + dates[i] + u";\"" +posty[i] + u"\"")
#codecs.open("")
const = (forum + ";" + thread + ";"+  title + ";").encode('utf8')


for post in posty:
	out = const + (authors.next() + ";").encode('utf-8')
	out += (dates.next() + ";").encode('utf-8')
	out += ("\""+post +"\"").encode('utf-8')
	print out

#print out



