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
#extracts thread title from soup tree
	titles = soup.find_all('a', 'titles')
	return rmDbQ(titles[0].string)

def getAuthors(soup):
	authors = soup.find_all('b','postauthor')
	authors_txt = []
	for auth in authors:
		authors_txt.append(auth.string)
	return authors_txt

def getDates(soup):
	dates_reg = re.compile("Napisane.+(\d{1,2})\s([^ ][^ ][^ ])\s(\d{4}), o (\d{1,2}):(\d{1,2})")
	matches = dates_reg.findall(str(soup.html))
	dates = []
	for date in matches:
		dates.append(formatDate(date))
	return dates
def getPost(soup):
	posts = soup.find_all("div","postbody")
	posts_txt = []
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
			posts_txt.append(rmDbQ(txt))
		prev_parent = current_parent
	return posts_txt

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

ipdb.set_trace()

for i in range(len(posty)):
	out = const + (authors[i]+";").encode('utf-8')
	out += (dates[i]+";").encode('utf-8')
	out += ("\""+posty[i]+"\"").encode('utf-8')
	print out

#print out



