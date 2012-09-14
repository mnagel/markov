#!/usr/bin/env python

import sys
from markov import MarkovChain

if len(sys.argv) != 2:
	print "usage:"
	print "python brownian.py $OUTLENGTH"
	print "example:"
	print "python brownian.py 300"
	sys.exit(1)

m = MarkovChain(1)

n = 1000
for i in range(-n + 1, n+1 - 1):
	m.observe_string("%d %d" % (i, i-1))
	m.observe_string("%d %d" % (i, i+1))

m.observe_string("%d %d" % ( n,  n))
m.observe_string("%d %d" % (-n, -n))

start = ["0"]

#result = m.random_walk_string(int(sys.argv[1]), start)
#print result

from pylab import *
result = m.random_walk(int(sys.argv[1]), start)
result = [int(x) for x in result]
plot(result)
show()
