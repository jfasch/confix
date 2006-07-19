#!/usr/bin/env python

# $Id: writedot.py,v 1.12 2006/06/21 12:20:10 jfasch Exp $

from libconfix.repofile import RepositoryFile
import libconfix.debug
from libconfix.pkg_installed import InstalledPackage
from libconfix.digraph.digraph import DirectedGraph
from libconfix.core.edgefinder import EdgeFinder
from libconfix.error import Error
from libconfix.helper_automake import automake_name
import sys

def write_graph(graph):

    lines = []

    lines.append('digraph my_wonderful_digraph {')

    # nodes

    for n in graph.nodes():
        lines.append('  '+automake_name('_'.join(n.fullname()))+\
                     '[label="'+'.'.join(n.fullname())+'"];')
        pass

    lines.append('')

    # edges

    for e in graph.edges():
        lines.append('  '+automake_name('_'.join(e.tail().fullname()))+' -> '
                     ''+automake_name('_'.join(e.head().fullname()))+';')
        pass

    lines.append('}')

    return lines


def main():
    libconfix.core.debug.set_trace('resolve')
    try:
        modules = []
        for filename in sys.argv[1:]:
            repo = RepositoryFile(filename)
            pkg = repo.load()
            assert isinstance(pkg, InstalledPackage)
            modules.extend(pkg.modules())
            pass
        
        graph = DirectedGraph(nodes=modules, edgefinder=EdgeFinder(nodes=modules))
        
        print '\n'.join(write_graph(graph))

    except Error, e:
        print `e`

if __name__ == "__main__":
    main()


