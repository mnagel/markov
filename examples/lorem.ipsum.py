#!/usr/bin/env python

import sys
from markov import MarkovChain

if len(sys.argv) != 4:
	print "usage:"
	print "python lorem.ipsum.py $ORDER $DATAFILE $OUTLENGTH"
	print "example:"
	print "python lorem.ipsum.py 3 data.txt 300"
	sys.exit(1)
	
order    = int(sys.argv[1])
filename = sys.argv[2]
length   = int(sys.argv[3])

m = MarkovChain(order)
m.observe_file(filename)
start = m.get_random_prestate()
result = m.random_walk_string(length, start)
print result
