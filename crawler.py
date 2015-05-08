# coding=utf-8
import sys
import re
from urllib2 import Request, urlopen, HTTPError, URLError
import urlparse
from bs4 import BeautifulSoup
import random

nfiles = 0
root = 'http://www.apostol.pl/forum/'
tocrawl = set([root])
crawled = set([])

##
## Reg exp do zadania: "Znajdz wszystkie fora" (nie uwzglednia ze strona glowna moze nie obejmowac wszystkich for, ale to rzadkie przypadki)

forumregex  = re.compile('viewforum.php\?f=(\d+)')
#####################################################
def __get(crawling):
	url = urlparse.urlparse(crawling)
	try:
		response = urlopen(crawling)
	except HTTPError, e:
		print "Request failed"
		print "Error : ",e.code
	except URLError, e:
		print e.reason
	return response.read()
	
#####################################################
def getForumNumbers(root, forumregex):
	#podnies ze stosu link
	#crawling = tocrawl.pop()
	#Zaraportuj co crawlujesz
	print root
	#zparsuj url

	#wczytaj htmla do zmiennej
	html = __get(root)
	#Znajdz numery wszystkich for
	fors = forumregex.findall(html)
	#zapisz ze to juz bylo crawlowane
	#crawled.add(crawling)
	#zwroc fora, ktore znalazles
	return fors

#######################################################

def getAllPages(Page):
	#regex do znajdywania threadow
	topicregex = re.compile('href="./(viewtopic.php.+)" class="topictitle"')
	
	print "Forum :" + Page
	html = __get(Page)
	topics = topicregex.findall(html)
#	print topics
	for topic in topics:
		rep = re.compile('&amp;')
		topic = rep.sub('&', topic)
		print "#TOPIC# " + topic
		getTopic(topic,0)
	soup = BeautifulSoup(html)
	#print html
	for elem in soup('a', text=u'Następna strona'):
		next = elem.get('href')
		if next:
			next = next[1:]
			getAllPages(root + next)
			break
#	next_page = elem.parent.get('href')
#	if(next_page):
#		print "Nastepna..."
#		getAllPages(page)
#	else:
#		print "Ostatnia!"

	return 1
	#print html
	#soup = BeautifulSoup(html)
	#watki_na_stronie = soup.a['topictitle']
	#print watki_na_stronie


###################################################################
def getTopic(topic,page):
	page = page + 1
	#print root+topic
	html = __get(root + topic)
	#print topic
	forumid_regex = re.compile('f=(\d+)&')
	m = forumid_regex.findall(topic)
	
	forumid = m[0]
	if forumid:
		print "Forum id:" + forumid
	else:
		die()
	topicid_regex = re.compile('t=(\d+)&')
	m = topicid_regex.findall(topic)
	topicid = m[0]

	if topicid:
		print "Topic id :" +topicid
	else:
		die()
	#startid_regex = re.compile('start=(\d+)')
	#m = startid_regex.findall(topic)
	#start = 0
	#if len(m)>0 :
	#	start = m[0]
	writePage(html, "Topic_"+forumid+"_"+topicid+"_p"+str(page) + ".html")

	soup = BeautifulSoup(html)
	for elem in soup('a',text=u'Następna strona'):
		next = elem.get('href')
		if next:
			next = next[2:]
			print "#!NEXT "+next
			getTopic(next,page)
			break
	return 0
########################################################################

def writePage(PageHtml, Name):
	global nfiles
#### zapisz na dysk strone z watku, zwroc nastepna strone z watku
#	open('apostol.pl/html/'+Name, 'w')
	#print "Plik:"+Name
	nfiles = nfiles +1
	print "File number " + str(nfiles)
	try:
		f = open('/home/mikolaj/Dokumenty/crawlerMK-pliki/apostol.pl/'+Name, "w")
		try:
			f.writelines(PageHtml)
		finally:
			f.close()
	except IOError:
		print "IO Error  "
		#pass
	return 0
##########################

def main():
### main
	numbers = getForumNumbers(root, forumregex)
	for fnumber in (numbers.pop(0) for _ in xrange(len(numbers))):
		if int(fnumber) > 10 and int(fnumber) not in [35,29,26,14,13,11,12]:
			print fnumber
			getAllPages(root + 'viewforum.php?f=' + fnumber)

main()	



