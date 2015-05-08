# coding=utf-8
import sys
import re
from urllib2 import Request, urlopen, HTTPError, URLError
import urlparse
from bs4 import BeautifulSoup

root = 'http://adonai.pl/zrodelko/'

#####################################################
class Crawler:
    ###########################
    def __get(self,crawling):
        if len(crawling)==0:
            print "blank link"
            sys.exit(0)
        url = urlparse.urlparse(crawling)
        try:
            response = urlopen(crawling)
        except HTTPError, e:
            print "Request failed"
            print "Error : ",e.code
        except URLError, e:
            print e.reason
        return response.read()
    ############################
    def __init__(self,root,dirname):
        self.root = root
        self.dirname = dirname
        self.content = self.__get(root)
        self.count = 0
        self.nextpage = False
        self.nextpage_link = ""
    ############################
    def __next(self,content):
        print "<next>"
        soup  = BeautifulSoup(content)
        nextpage = False
        match = re.findall(r'\[<a href="([^\]]+)">><\/a>\]',content)
        if match:
            self.nextpage_link  =self.root +match[0]
            return True
        print "</next>"
        return False 
    ############################
    def walk(self): 
        print "<walk>"
        self.nextpage = True
        while 1:
            self.nextpage = self.__next(self.content)
            print self.nextpage
            if self.nextpage:
                self.content = self.__get(self.nextpage_link)
                self.count += 1
                self.page_name = str(self.count) + ".html"
                self.writepage()
            else:
                break
        print "</walk>"
    ############################
    def writepage(self):
        try:
            f = open(self.dirname+'/'+self.page_name, "w")
            try:
                f.writelines(self.content)
            finally:
                f.close()
        except IOError:
            print "IO Error"
            sys.exit(0)

########################################################


def main():
    adn = Crawler('http://adonai.pl/zrodelko/','adonai.pl')
    print adn.content[:20]
    adn.walk()


if __name__ == '__main__':
    main()

