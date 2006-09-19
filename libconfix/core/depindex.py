# $Id: depindex.py,v 1.5 2006/06/27 15:09:00 jfasch Exp $

# Copyright (C) 2005 Salomon Automation

# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of the
# License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

from provide_string import Provide_String

from libconfix.core.repo.marshalling import Unmarshallable
from libconfix.core.utils.error import Error

class ProvideMap(Unmarshallable):

    def __init__(self, permissive):

        # permissive means to return as soon as we have at least one
        # match (to return as soon as possible, so to say), and to not
        # continue to search for more.

        self.permissive_ = permissive

        # dictionary: require-type -> Index_Provide_String

        self.string_indexes_ = {}

        # list of tuples (provide-object, Node)
        
        self.rest_ = []

    def find_match(self, require):

        # see if a string index claims to know how to match the
        # require

        ret_nodes = []

        index = self.string_indexes_.get(require.__class__)
        if index:
            ret_nodes.extend(index.find_match(require))
            if self.permissive_ and len(ret_nodes) > 0:
                return ret_nodes
            pass

        # ask the anti-performant section for a match.

        for p, n in self.rest_:
            if p.resolve(require):
                ret_nodes.append(n)
                if self.permissive_ and len(ret_nodes) > 0:
                    return ret_nodes
                pass
            pass

        return ret_nodes
        
    def add(self, provide, node):

        # if the provide object is not one which we can index
        # (Provide_String is the only indexable so far), then add it
        # to the anti-performant section.

        if not isinstance(provide, Provide_String):
            self.rest_.append((provide, node))
            return

        # else, create an index for its type (if not yet available),
        # and add it there.

        for require_type in provide.can_match_classes():
            index = self.string_indexes_.get(require_type)
            if not index:
                index = Index_Provide_String(type=require_type,
                                             permissive=self.permissive_)
                self.string_indexes_[require_type] = index
                pass
            index.add(provide, node)
            pass
        pass

class Index_Provide_String(Unmarshallable):

    def __init__(self,
                 type,
                 permissive):

        # the type of the provide objects that I am responsibe for

        self.type_ = type

        # same meaning as with our checf, the ProvideMap

        self.permissive_ = permissive

        # map string -> Node

        self.exact_ = {}

        # list of tuples (prefix-provide, node) 
        
        self.prefix_ = []

        # list of tuples (prefix-provide, node)
        
        self.glob_ = []

        pass

    def n_exact(self): return len(self.exact_)
    def n_prefix(self): return len(self.prefix_)
    def n_glob(self): return len(self.glob_)

    def find_match(self, require):

        """ Try to match the given require object against what I have.

        @return: A Node object if one is found, else None """

        ret_nodes = []

        node = self.exact_.get(require.string())
        if node:
            ret_nodes.append(node)
            pass

        if self.permissive_ and len(ret_nodes) > 0:
            return ret_nodes

        for p, n in self.glob_:
            if p.resolve(require):
                ret_nodes.append(n)
                if self.permissive_:
                    return ret_nodes
                pass
            pass

        for p, n in self.prefix_:
            if p.resolve(require):
                ret_nodes.append(n)
                if self.permissive_:
                    return ret_nodes
                pass
            pass

        return ret_nodes

    def add(self, provide, node):
        if provide.match() == Provide_String.EXACT_MATCH:
            existing_node = self.exact_.get(provide.string())
            if existing_node:
                raise Error('Index for provide type "'+self.type_.__name__+'": '
                            'duplicate provide-key "'+provide.string()+'", '
                            'conflicting parties are '+str(node)+' and'
                            ' '+str(existing_node))
            self.exact_[provide.string()] = node
        elif provide.match() == Provide_String.PREFIX_MATCH:
            self.prefix_.append((provide, node))
        elif provide.match() == Provide_String.GLOB_MATCH:
            self.glob_.append((provide, node))
