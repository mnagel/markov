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

min, max = -999, +999
for i in range(min, max+1):
	m.observe(  (str(i),)  ,  str(i-1)  )
	m.observe(  (str(i),)  ,  str(i+1)  )

m.observe(  (str(min-1),)  ,  str(min-1)  )
m.observe(  (str(max+1),)  ,  str(max+1)  )

start = ["0"]

#result = m.random_walk_string(int(sys.argv[1]), start)
#print result

from pylab import *
result = m.random_walk(int(sys.argv[1]), start)
result = [int(x) for x in result]
plot(result)
show()
