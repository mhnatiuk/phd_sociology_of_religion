import csv
import math
from sys import argv
from collections import defaultdict
## This script calculates TF/IDF value for words in a set of documents
## User has to specify:
## 1. A csv-formatted file (';' as separator, '"' as quote),
## 2. The number of a column which contains words (from 1 not 0)
## 3. The number of a column which contains the sum of term occurances in a document (from 1 not 0)
## 4. The number of a column that indicates by which column to aggregate ( a document : 'd' in http://en.wikipedia.org/wiki/TFIDF ) (from 1 not 0)
## This script writes output to STDOUT
##

try:
    sname, filename, w_col, sum_col, a_col, add1, add2 = argv
except ValueError:
        quit("Please try: script.py filename column-with-words column-to-aggregate-by")

try:
    w_col= int(w_col)-1
    sum_col= int(sum_col) -1
    a_col= int(a_col) -1 # aggregate
    add1 = int(add1) - 1 # data
    add2 = int(add2) - 1 # temat
except ValueError:
    quit("Last 3 arguments must be integers")



with open(filename, "r") as csvfile:
    reader = csv.reader(csvfile,delimiter=';',quotechar='"')
    docs = dict()
    docfreq = defaultdict(dict) # number of documents where the term T appears
    termfreq = defaultdict(int) # term frequency per document

    additional = defaultdict(list)

    max_term = 1 # maximum frequency of any term in document (adjusted tf)
    for row in reader:
        #print "col: ", row[a_col]
        if row[sum_col] > max_term:
            max_term = int(row[sum_col])
        #for every TERM, write number of documents where it appears:
        ### TOFIX ###
        #docfreq[row[w_col]][row[a_col]] += 1
        docfreq[row[w_col]][row[a_col]] = 1

        # just keep track of the number of documents:
        docs[row[a_col]] = 1

        #add word freq to the dictionary of terms in documents
        key = (row[w_col], row[a_col])
        termfreq[key] = int(row[sum_col])

        ##addtional info
        additional[row[a_col]] = [row[add1], row[add2]]

    D = len(docs) # total no documents

#    sum_of_words_in_doc = defaultdict(int)
#    for keys,val in termfreq.iteritems():
#        sum_of_words_in_doc[keys[1]] += val

    # calculate and print TF/IDF value:
    for keys, val in termfreq.iteritems():
        term = keys[0]
        doc = keys[1]
        data = additional[doc][0]
        temat = additional[doc][1]
#        tf = float(termfreq[keys]) / sum_of_words_in_doc[doc]
        tf = float(termfreq[keys])
        #tf = 0.5 + ( (0.5 * termfreq[keys]) / (max_term) )

        no_docs_with_term = float(len(docfreq[term]))
        #print "Licznik",float(D), "Mianownik", no_docs_with_term
        assert float(D) >= no_docs_with_term, \
            "%s - %s" % (float(D), no_docs_with_term)
            ### assert that number of all documents is ALWAYS gr or eq
            # than the number of documents that contain the term
        quotient =  float(D) / no_docs_with_term
        if quotient < 1:
            raise ValueError, "(Number of documents / Number of documents with term x) is less than 1!"
        #print "ROW",quotient, D, no_docs_with_term
        idf = math.log( quotient )
        tfidf = tf * idf
        assert tfidf >= 0
        #dictTFIDF[keys] = tfidf
        print '"%s";"%s";%f;%f;%f;"%s";"%s"' % (term,doc,tfidf,tf, no_docs_with_term, data, temat)
        #print "In document %s term %s has tfidf value of %r" % (doc, term, tfidf)

    #D # number of documents in the corpus
    #tf #per document, so its length is equal to the number of rows in csv file
    #idf #per term, so its length equal to the number of unique words in csv file




