import csv
import numpy as np
import scipy as sp
from sys import argv


def aggregate(df, by=0,to=1,func=np.sum):
	Dat = dict()
	ColBy = df.T[by]
	ColTo = df.T[to]
	ColToInt = []
	for i in range(0,len(ColTo)):
		ColToInt.append(int(ColTo[i]))
	#print "By : %r " % (ColBy)
	#print "To : %r " % (ColToInt)
	ColTo = np.array(ColToInt)
	UniqueBy = np.sort(np.unique(ColBy))
	for ub in UniqueBy:
		#print ub
		uTo = ColTo[ColBy==ub]
		Out =func(uTo)
		#print Out
		Dat[ub] = Out
		#Dat.append(np.concatenate(([ub],Out)))
	return Dat



try:
        sname, fname = argv
except ValueError:
        quit("Err: pass a filename.")

with open(fname, "r") as csvfile:
        reader = csv.reader(csvfile,delimiter=';',quotechar='"')
	data = []
	for row in reader:
		data.append([row[1] + ";" + row[2] + ";" +row[6], row[7] ] ) 

	out = aggregate(np.array(data))
	for k,v in out.iteritems():
		print "%s;%s" %(k,v)
	#data = aggregate(reader, )
