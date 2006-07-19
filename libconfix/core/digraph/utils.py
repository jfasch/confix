# $Id: utils.py,v 1.1 2006/06/27 15:08:59 jfasch Exp $

from libconfix.core.utils.error import Error

from digraph import DirectedGraph, Edge

import toposort

def reached_from(digraph, entrypoints):

    unique_nodes = set()

    for e in entrypoints:
        for n in toposort.toposort(digraph, e):
            unique_nodes.add(n)

    edges = []
    for tail in unique_nodes:
        for head in digraph.successors(tail):
            edges.append(Edge(tail=tail, head=head))

    return DirectedGraph(nodes=[n for n in unique_nodes], edges=edges)

def subgraph(digraph, nodes):

    """ From digraph, select nodes and remaining edges to form a new
    digraph. Return the new digraph. """

    return DirectedGraph(
        nodes=nodes,
        edges=select_containing_edges(nodes=nodes,
                                      edges=digraph.edges()))

def subtract(digraph, nodes):

    """ Subtract nodes from digraph, together with the affected
    edges. Return resulting digraph. """

    remaining_nodes = set(digraph.nodes()) - set(nodes)
    return DirectedGraph(
        nodes=remaining_nodes,
        edges=select_containing_edges(nodes=remaining_nodes,
                                      edges=digraph.edges()))
    
def select_containing_edges(nodes, edges):

    """ From edges, select those whose ends are members of nodes (and
    return them). """

    node_set = set(nodes)
    ret_edges = []

    for e in edges:
        if e.head() in node_set and e.tail() in node_set:
            ret_edges.append(e)
            pass
        pass

    return ret_edges
