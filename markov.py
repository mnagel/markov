#!/usr/bin/env python

# inspired by
# http://de.wikipedia.org/wiki/Markow-Kette
# http://www.aiplayground.org/artikel/markov/
# https://github.com/vedant/markov-chain-generator/

from collections import defaultdict
import logging
log = logging
import random
import sys

class MarkovChain(object):
	"""
	generate pseudo-random texts based on markov chains
	
	- calculates how likely a certain words follow a given word or phrase
	- (use an existing text to determine the probabilities)
	- start with an initial word or phrase
	- do a random walk over the "space of words"
	- when choosing the next word, respect the determined probabilities
	- obtain a meaningless text that somewhat resemebles the original text
	"""

	def __init__(self, order):
		"""
		create a new instance of MarkovChain
		This class basically stores the observed transitions
		and provides a container for the related methods.
		
		Documentation of the internal Data Structures
		---------------------------------------------
		
		transitions
		-----------
		a hash (multi-map) from prestate to poststate.
		prestate is a n-tuple of previous states.
		n depends on (i.e. equals) the order of the markov chain.
		poststate is a single state.
		
		currently a state is simply a string.
		
		For every occurrence of prestate followed by poststate
		in the initialization (observation) phase, the mapping
		(prestate: poststate)
		is appended to the transitions hash.
		If the transition from some prestate to some poststate
		is observed multiple times, this transition is inserted multiple times.
		There is no "counting" or other optimization.
		
		order
		-----
		the order of the markov chain.
		For n == 1 the previous state is considered as prestate in transitions.
		For n == 2 the previous state and the state before that is considered.
		...
		
		"""
		self.transitions = defaultdict(list)
		self.order = order

	def observe(self, prestate, poststate):
		"""
		add a single oberservation to transitions
		
		prestate  - a tuple of states
		poststate - a single state
		"""
		log.debug("%s -> %s" % (str(prestate), str(poststate)))
		self.check_prestate(prestate)
		self.transitions[prestate].append(poststate)

	def state_iterator(self, states):
		"""
		iterate over all n-tupels in a list of states
		
		Yields a tuple (prestate, poststate)
			where
				prestate  - is tuple of states
				poststate - is a single state
		
		states - a list (not a tuple) of states
		"""
		# n-tupels only start at these idx'es
		for idx_start in range(len(states) - self.order):
			# yield a list of self.order elements starting at idx_start
			prestate = states[idx_start : idx_start + self.order]
			poststate = states[idx_start + self.order]
			yield (prestate, poststate)

	def observe_all(self, states):
		"""
		add all observations in a list of states
		
		states - a list (not a tuple) if states
		"""
		log.debug("%s" % (str(states)))
		for tup in self.state_iterator(states):
			prestate = tup[0]
			prestate = tuple(tup[0]) # make immutable
			poststate = tup[1]
			self.observe(prestate, poststate)

	def observe_string(self, string):
		"""
		add all observations in a string
		
		string - the string of observation.
		The string is split at word boundaries
		and each word is considered as the observation of a state.
		"""
		string = string.lower()
		log.debug("%s" % string)
		self.observe_all(string.split())

	def observe_file(self, filename):
		"""
		load a string of observations from a file
		
		filename - path to the file to load
		"""
		log.debug("%s" % filename)
		linestring = open(filename, "r").read()
		linestring = linestring.lower()
		self.observe_string(linestring)

	def random_step(self, prestate):
		"""
		do one transition from the prestate
		
		prestate - a tuple, the prestate where to start.
		The class does not keep track of a current "position",
		so this must be passed as a parameter.
		"""
		self.check_prestate(prestate)
		prestate = tuple(prestate) # make immutable
		if not prestate in self.transitions:
			raise Exception("reached dead end with prestate: %s" % (str(prestate)))
		result = random.choice(self.transitions[prestate])
		log.debug("%s -> %s" % (str(prestate), str(result)))
		return result

	def random_walk(self, length, init):
		"""
		do a random walk on the state space
		
		length - one so many transitions are simulated
		init   - a list, denoting the initial history of state(s).
		This should be a "valid" tuple, i.e. there should exist some transitions
		to "move away" from this state.
		"""
		log.debug("%d %s" % (length, str(init)))
		self.check_prestate(init)
		state = init
		for i in xrange(length):
			prestate = state[i : i + self.order]
			next = self.random_step(prestate)
			state.append(next)
		return state

	def random_walk_string(self, length, init):
		"""
		wrapper for random_walk that returns a joined string
		"""
		log.debug("%d %s" % (length, str(init)))
		result = self.random_walk(length, init)
		return " ".join(result)

	def get_random_prestate(self):
		"""
		return a valid prestate in the correct list format
		"""
		prestate = random.choice(self.transitions.keys())
		self.check_prestate(prestate)
		return list(prestate)

	def check_prestate(self, prestate):
		"""
		check if a prestate if valid (has correct order)
		
		prestate - a list or tuple to check
		"""
		if len(prestate) != self.order:
			raise Exception("prestate is not of correct order")
		else:
			return True

