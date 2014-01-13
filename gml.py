"""Library to parse the OGDF GML file format."""
# GML Parsing library for the ubigraph trace generation
# Written by Danny Quist, Open Malware
# Copyright (C) 2013 Danny Quist
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import re, sys

nodeStartre = re.compile("node \[")
edgeStartre = re.compile("edge \[")
graphicsStartre = re.compile("graphics \[")
endBlockre = re.compile("\]")
sourcere = re.compile("source (\d+)")
targetre = re.compile("target (\d+)")
idre = re.compile("id (\d+)")
labelre = re.compile("label \"<label.*>([0-9a-fA-F]+)</label>")
fillre = re.compile("fill \"#([a-fA-F0-9]+)\"")

class Node:
    def __init__(self, id=None, label=None, color=None, coords=(0,0,0)):
        self.x = coords[0]
        self.y = coords[1]
        self.z = coords[2]
        self.id = int(id)
        self.label = label
        self.color = color

class Edge:
    def __init__(self, src, dst, width=None):
        self.srcid = int(src)
        self.dstid = int(dst)
        self.width = width

class Graph:
    def __init__(self, gmlfile=None, delayedLoad=False):
        self.gmlfile = gmlfile
        self.nodes = {}
        self.edges = []

        if gmlfile and not delayedLoad:
            self.open()

    def open(self, gmlfile=None):
        if gmlfile:
            fin = open(gmlfile, 'r')
        elif self.gmlfile:
            fin = open(self.gmlfile, 'r')
        else:
            raise "No file specified"
        
        l = fin.readline()

        inNode = False
        inGraphics = False
        inEdge = False

        id = None
        label = None
        fill = None

        src = None
        dst = None

        while (l):
            if nodeStartre.match(l):
                inNode = True
            elif edgeStartre.match(l):
                inEdge = True

            if inNode and not inGraphics:
                idm = idre.match(l)
                labelm = labelre.match(l)
                graphicsm = graphicsStartre.match(l)
                endblockm = endBlockre.match(l)

                if idm:
                    id = idm.group(1)
                elif labelm:
                    label = labelm.group(1)
                elif graphicsm:
                    inGraphics = True
                elif endblockm:
                    inNode = False
                    self.nodes[int(id)] = Node(id=id, label=label, color=fill)
                    #self.nodes.append( Node(id=id, label=label, color=fill) )
                    id = label = fill = None

            elif inNode and inGraphics:

                endblockm = endBlockre.match(l)
                fillm = fillre.match(l)

                if fillm:
                    fill = fillm.group(1)
                elif endblockm:
                    inGraphics = False

            if inEdge and not inGraphics:

                endblockm = endBlockre.match(l)
                sourcem = sourcere.match(l)
                targetm = targetre.match(l)
                graphicsm = graphicsStartre.match(l)

                if sourcem:
                    src = sourcem.group(1)
                elif targetm:
                    dst = targetm.group(1)
                elif graphicsm:
                    inGraphics = True
                elif endblockm:
                    inEdge = False
                    self.edges.append(Edge(src=src, dst=dst))
                    src = dst = None

            if inEdge and inGraphics:

                endblockm = endBlockre.match(l)

                if endblockm:
                    inGraphics = False

            l = fin.readline()

        fin.close()

        
