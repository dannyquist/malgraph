#!/usr/bin/python

import sys
import os
import gml


def usage():
    print "gmltocsv.py - Part of the malgraph toolkit"
    print "Copyright (C) 2014 Daniel Quist, All Rights Reserved\n"
    print "Usage: gmltocsv.py [infile] [outfile (optional)]"
    print "If no outfile is present, stdout is used for output"

def main(argv):
    infile = None
    infile_name = None
    outfile = None
    outfile_name = None

    if len(argv) == 1:
        usage()
        sys.exit(1)
    elif len(argv) == 2:
        infile = open(argv[1], 'r')
        infile_name = argv[1]
        outfile = sys.stdout
    elif len(argv) == 3:
        infile = open(argv[1], 'r')
        infile_name = argv[1]
        outfile = open(argv[2], 'w')
        outfile_name = argv[2]
    else:
        usage()
        sys.exit(2)

    g = gml.Graph(infile_name)

    for e in g.edges:
        print >>outfile, "%d;%d" % (e.srcid, e.dstid)

    if infile != sys.stdin:
        infile.close()

    if outfile != sys.stdout:
        outfile.close()


if __name__ == '__main__':
    main(sys.argv)
