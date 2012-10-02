#!/usr/bin/env python

import sys
from markov import MarkovChain

def spacer():
	print "-" * 60

order    = 1
length   = 50

text = """
	g8 e8 e4 f8 d8 d4
	c8 d8 e8 f8 g8 g8 g4
	g8 e8 e4 f8 d8 d4
	c8 e8 g8 g8 c4 r4
	g8 e8 e4 f8 d8 d4
	c8 d8 e8 f8 g8 g8 g4
	g8 e8 e4 f8 d8 d4
	c8 e8 g8 g8 c4 r4
"""

m = MarkovChain(order)

print "observing %s" % text
spacer()
m.observe_string(text)
print "TODO make logging verbose for observe()..."

spacer()
m.print_transitions()
spacer()
m.print_matrix()

start = m.get_random_prestate()
spacer()
result = m.random_walk_string(length, start)

print result
