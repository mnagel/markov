#!/usr/bin/env python

import random
import re
import string
import subprocess
import sys
import os

"""
if len(sys.argv) != 5:
	print "usage:"
	print "python algorithmic.music.py $ORDER $TEMPLATEFILE $DATAFILE $OUTLENGTH"
	print "example:"
	print "python algorithmic.music.py 1 data/lilypond-template.ly data/entchen.ly 300"
	sys.exit(1)
"""

#order    = int(sys.argv[1])
template = sys.argv[1]
filename = sys.argv[2]
#length   = int(sys.argv[4])

lilypond = "lilypond"
if sys.platform.startswith("darwin"):
	lilypond = "/Applications/LilyPond.app/Contents/Resources/bin/lilypond"

rand = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))

linestring = open(filename, "r").read()

output = open(template, 'r').read()
title = "Lilypond: %s" % (os.path.basename(filename))
output = re.sub("%%%TITLE-GOES-HERE%%%", title, output)
output = re.sub("%%%CONTENT-GOES-HERE%%%", linestring, output)

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

subprocess.call(["xdg-open", pdfpath])
subprocess.call(["xdg-open", midipath])
