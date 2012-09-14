#!/usr/bin/env python

import sys
from markov import MarkovChain

order    = 2
length   = 500

text = """
	g'8 e'8 e'4 f'8 d'8 d'4
	c'8 d'8 e'8 f'8 g'8 g'8 g'4
	g'8 e'8 e'4 f'8 d'8 d'4
	c'8 e'8 g'8 g'8 c'4 r4
	g'8 e'8 e'4 f'8 d'8 d'4
	c'8 d'8 e'8 f'8 g'8 g'8 g'4
	g'8 e'8 e'4 f'8 d'8 d'4
	c'8 e'8 g'8 g'8 c'4 r4
"""

m = MarkovChain(order)
m.observe_string(text)
m.print_matrix()
start = m.get_random_prestate()
result = m.random_walk_string(length, start)
print result
