#!/usr/bin/env python

import random
import re
import string
import subprocess
import sys
import os

from markov import MarkovChain

if len(sys.argv) != 5:
	print "usage:"
	print "python algorithmic.music.py $ORDER $TEMPLATEFILE $DATAFILE $OUTLENGTH"
	print "example:"
	print "python algorithmic.music.py 1 data/lilypond-template.ly data/entchen.ly 300"
	sys.exit(1)

order    = int(sys.argv[1])
template = sys.argv[2]
filename = sys.argv[3]
length   = int(sys.argv[4])

lilypond = "lilypond"
opencmd = "xdg-open"
if sys.platform.startswith("darwin"):
	lilypond = "/Applications/LilyPond.app/Contents/Resources/bin/lilypond"
	opencmd = "open"

m = MarkovChain(order)
m.observe_file(filename, True)
start = m.get_random_prestate()
result = m.random_walk(length, start)


def tactify(tuplelist, resolution, tact):
  # tuplelist: eingabeliste
  # resolution: kleinste note
  # tact: wieviele resolution-noten einen takt geben (ignored)

  # immer 4/4 Takt
  takt = resolution # in 16teln
  count = 0
  output = []

  pos = 0

  copy = tuplelist[:] # copy, so we do not destoy
  tuplelist = copy

  while pos < len(tuplelist):
    t = tuplelist[pos]
    matchObj = re.match(r'([^0-9]*)([0-9]*)', t)
    tname = matchObj.group(1)
    print t
    tleng = takt / int(matchObj.group(2))
    print t, tname, str(tleng)
    if count + tleng <= takt:
      output.append(tname + str(takt/tleng))
      if count + tleng == takt:
        count = 0
      else:
        count = count + tleng
    else:
      tleng = tleng/2
      print "split to " + str(tleng)
      tuplelist[pos] = tname + str(takt/tleng)
      tuplelist.insert(pos+1, tuplelist[pos])
      pos -= 1 # keine Note endgueltig verarbeitet
    pos += 1
  return output

m.print_matrix()
print result
result = tactify(result, 16, None)
result = " ".join(result)

output = open(template, 'r').read()
title = "markov.py: %s @%d" % (os.path.basename(filename), order)
output = re.sub("%%%TITLE-GOES-HERE%%%", title, output)
output = re.sub("%%%CONTENT-GOES-HERE%%%", result, output)

rand = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))

folder = os.path.dirname(template) + "/work/"
lilypondfile = rand + ".ly"
lilypondpath = folder + lilypondfile
midipath = folder + rand + ".midi"
pdfpath = folder + rand + ".pdf"

with open(lilypondpath, "w+") as text_file:
    text_file.write(output)

print "lilypond input file created: %s" % lilypondpath

cmd = ["bash", "-c", "cd %s && %s %s" % (folder, lilypond, lilypondfile)]
print "running lilypond as: \n%s" % (" ".join(cmd))

print "-" * 60
subprocess.call(cmd)
print "-" * 60

print "lilypond finished, opening output files"

subprocess.call([opencmd, pdfpath])
subprocess.call([opencmd, midipath])
