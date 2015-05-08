#-*- coding: utf-8 -*-

import re
import morfeusz
import csv
import nltk
from collections import defaultdict
from sys import stderr
from sys import argv
from time import time
####################
def get_word_counts(text):
    words = defaultdict(int)
    tokens = nltk.wordpunct_tokenize(text)
    for word in tokens: # for every word in given text -> lemmatize & count
        word = re.sub(r'[_+=:;"\'\?/>.<,\\]',' ',word)
        if len(word) > 1:
            #print word.encode('utf8')
            res =  morfeusz.analyse(word,expand_tags=False,dag=True) # morfological analyzer for Polish
            try:
                base = res[0][2][1]
            except IndexError:
                base = None
            #list.append(tup[1])
            if base is not None:
                words[base] += 1 # increment the word count
            else:
                pass
    return words

#################
def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]
#############################################################3

try:
    sname, fname, column = argv
except ValueError:
    quit("Err: pass a filename.")

column = int(column)

with open(fname, "r") as csvfile:
    reader = unicode_csv_reader(csvfile,delimiter=';',quotechar='"')
    start = time()
    i= 0
    for row in reader:
        if i % 1000 == 0:
            print >> stderr, "%d rows read in %f" % (i, time() -start)
        i += 1
        try:
            rows_returned = get_word_counts(row[column])
        except IndexError:
            next

        for k,v in rows_returned.iteritems():
            out = '"' + '";"'.join(row[:column]  ) + '";' +  u'"' + k + u'";"' + unicode(v) + '"'
            print out.encode('utf8')
    end = time()

#    print "Exec time: %r"% (end - start)




#read whole file -  for big files You might want to change this to buffer-wise reading


