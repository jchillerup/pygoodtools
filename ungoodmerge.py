#!/usr/bin/env python2

import sys, os, glob, string
import pylzma
from py7zlib import *

needle_cascade = [
    "[!]", # We only want perfect dumps
    ["(E)", "(U)", "(J)"], # We prefer European, but we can live with American dumps if a perfect Euro doesn't exist
    ]

def reduce_list(inlist, needle):
    return [x for x in inlist if string.find(x, needle) != -1]
    

def pick_versions(candidates, cascade):
    for needle in cascade:
        # If the needle is a string we must obey
        if (type(needle) == str):
            candidates = reduce_list(candidates, needle)
        elif(type(needle) == list):
            # We initialize reduced to the empty list because we have an empty candidate set if none of
            # the priorities are matched.
            reduced = []
            
            for priority in needle:
                reduced = reduce_list(candidates, priority)

                # If we found at least one match, we're good, otherwise keep looping
                # BUG: if a ROM contains more than one title, we're not taking those into account here.
                if (len(reduced) > 0):
                    break;
                
            candidates = reduced

    return candidates

        
if (len(sys.argv) < 2):
    print "Usage: %s sourcedir [destdir]" % sys.argv[0]

source_directory = sys.argv[1]
destination_directory = sys.argv[2]

print "UnGoodMerge.py"
print "Unmerging from %s to %s" % (source_directory, destination_directory)

for infile in glob.glob(os.path.join(source_directory, "*.7z")):
    print "+ Processing %s..." % infile
    fp = open(infile, "rb")
    rom = Archive7z(fp)

    candidates = pick_versions(rom.getnames(), needle_cascade)

    for candidate in candidates:
        vfp = rom.getmember(candidate)
        vout = open(os.path.join(destination_directory, candidate), "wb")
        vout.write(vfp.read())
        print "  - %s" % candidate
