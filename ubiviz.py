#!/usr/bin/python
#
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

import sys, os, string, re, xmlrpclib, time

import gml

def main(argv):
    if len(argv) == 1:
        print "Usage: %s [gml file(s)]" % argv[0]
        sys.exit(1)
        
    for x in argv[1:]:
        print x
        displayGraph(x)
        time.sleep(8)

def displayGraph(gmlfile):
    g = gml.Graph(gmlfile)

    url = 'http://127.0.0.1:20738/RPC2'
    server = xmlrpclib.Server(url)
    G = server.ubigraph

    # Clear the graph
    G.clear()
    
    for n in g.nodes.keys():
        v = g.nodes[n]
        G.new_vertex_w_id(v.id)
        G.set_vertex_attribute(v.id, 'color', "#" + v.color)
        if "deadbeef" in v.label:
            G.set_vertex_attribute(v.id, 'label', 'START')

    for e in g.edges:
        #G.new_vertex_w_id(e.srcid)
        #G.set_vertex_attribute(e.srcid, 'color', "#" + g.nodes[e.srcid].color)
        #if "deadbeef" in g.nodes[e.srcid].label:
        #    G.set_vertex_attribute(e.srcid, 'label', 'START')
            
        #G.new_vertex_w_id(e.dstid)
        #if "deadbeef" in g.nodes[e.dstid].label:
        #    G.set_vertex_attribute(e.dstid, 'label', 'START')

        edge = G.new_edge(e.srcid, e.dstid)
        #G.set_edge_attribute(edge, 'spline', 'true')
        #G.set_edge_attribute(edge, 'arrow', 'true')
    

if __name__ == '__main__':
    main(sys.argv)
