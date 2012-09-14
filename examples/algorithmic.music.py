#!/usr/bin/env python

import sys
from markov import MarkovChain

if len(sys.argv) != 5:
	print "usage:"
	print "python lorem.ipsum.py $DATAFILE $ORDER $OUTLENGTH"
	print "example:"
	print "python lorem.ipsum.py data.txt 3 300"
	sys.exit(1)

order    = int(sys.argv[1])
template = sys.argv[2]
filename = sys.argv[3]
length   = int(sys.argv[4])

m = MarkovChain(order)
m.observe_file(filename)
start = m.get_random_prestate()
result = m.random_walk_string(length, start)

wrapper = open(template, 'r').read()

import re
import random
import string
import os

output = re.sub("%%%CONTENT-GOES-HERE%%%", result, wrapper)

randpart = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))

folder = os.path.dirname(template) + "/work/"
file = randpart + ".ly"
tempname = folder + file
midiname = os.path.dirname(template) + "/work/" + randpart + ".midi"

print tempname


with open(tempname, "w+") as text_file:
    text_file.write(output)
    
import sys
lp = "lilypond"
if sys.platform.startswith("darwin"):
	lp = "/Applications/LilyPond.app/Contents/Resources/bin/lilypond"

cmd = ["bash", "-c", "cd %s && %s %s" % (folder, lp, file)]
print "running"
print " ".join(cmd)

from subprocess import call
call(cmd)

print "created"

call(["open", midiname])
