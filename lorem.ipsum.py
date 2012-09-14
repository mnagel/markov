#!/usr/bin/env python

import sys
from markov import MarkovChain

if len(sys.argv) != 4:
	print "usage:"
	print "python lorem.ipsum.py $DATAFILE $ORDER $OUTLENGTH"
	print "example:"
	print "python lorem.ipsum.py data.txt 3 300"
	sys.exit(1)
	
order    = int(sys.argv[2])
filename = sys.argv[1]
length   = int(sys.argv[3])

m = MarkovChain(order)
m.observe_file(filename)
m.print_matrix()
start = m.get_random_prestate()
result = m.random_walk_string(length, start)
print result
