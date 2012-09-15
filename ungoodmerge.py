#!/usr/bin/env python2

import sys, os, glob, string
import pylzma
from py7zlib import *

needles = ["[!]", # Perfect dumps
           "(E)", # Europe
          ]


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

    # Gets all the version from the ROM
    for version in rom.getnames():
        this_version_good = True

        # Make sure the version passes all needles
        for needle in needles:
            if (string.find(version, needle) == -1):
                this_version_good = False
                break

        if (this_version_good == True):
            vfp = rom.getmember(version)
            vout = open(os.path.join(destination_directory, version), "wb")
            vout.write(vfp.read())
            print "  - %s" % version
    
