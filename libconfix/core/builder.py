# $Id: builder.py,v 1.16 2006/07/13 20:27:24 jfasch Exp $

# Copyright (C) 2002-2006 Salomon Automation

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

from depinfo import DependencyInformation
from iface import InterfacePiece
from provide_string import Provide_String
from require import Require
from buildinfoset import BuildInformationSet

from libconfix.core.utils.error import Error

import os

class Builder:
    def __init__(self, id, parentbuilder, package):
        self.id_ = id
        self.parentbuilder_ = parentbuilder
        self.package_ = package

        self.dep_info_ = DependencyInformation()
        self.num_announced_dep_info_ = 0

        self.buildinfos_ = BuildInformationSet()

        # flags to ensure that every derived builder's methods have
        # called their immediate base's methods that they overload,
        # and that the chain did reach the base of all builders.
        self.base_enlarge_called_ = False
        self.base_relate_called_ = False
        
        pass
    
    def id(self): return self.id_
    def __str__(self): return self.id_

    def parentbuilder(self):
        return self.parentbuilder_
    def package(self):
        return self.package_

    def add_require(self, r):
        self.dep_info_.add_require(r)
        pass
    def add_provide(self, p):
        self.dep_info_.add_provide(p)
        pass
    def add_internal_provide(self, p):
        self.dep_info_.add_internal_provide(p)
        pass
    def requires(self):
        return self.dep_info_.requires()
    def provides(self):
        return self.dep_info_.provides()
    def dependency_info(self):
        return self.dep_info_

    def add_buildinfo(self, b):
        self.buildinfos_.add(b)
        pass

    def buildinfos(self):
        return self.buildinfos_
    
    def iface_pieces(self):
        return [InterfacePiece(globals={'BUILDER_': self,
                                        'URGENCY_IGNORE': Require.URGENCY_IGNORE,
                                        'URGENCY_WARN': Require.URGENCY_WARN,
                                        'URGENCY_ERROR': Require.URGENCY_ERROR,
                                        'EXACT_MATCH': Provide_String.EXACT_MATCH,
                                        'PREFIX_MATCH': Provide_String.PREFIX_MATCH,
                                        'GLOB_MATCH': Provide_String.GLOB_MATCH},                               
                               lines=[builder_code_])]
    def makefile_py_iface_pieces(self):
        return []
    def enlarge(self):
        self.base_enlarge_called_ = True
        if self.num_announced_dep_info_ < self.dep_info_.size():
            diff = self.dep_info_.size() - self.num_announced_dep_info_
            self.num_announced_dep_info_ = self.dep_info_.size()
            return diff
        return 0
    
    def nodes(self):
        return []
    
    def relate(self, node, digraph, topolist):
        self.base_relate_called_ = True
        pass

    def output(self):
        pass


    # these are mainly for use by test programs
    def base_enlarge_called(self): return self.base_enlarge_called_
    def base_relate_called(self): return self.base_relate_called_
    
    pass


class BuilderSet:
    def __init__(self):
        # dictionary: builder id->builder
        self.builders_ = {}
        pass

    def __iter__(self):
        return self.builders_.itervalues()

    def __contains__(self, b):
        return self.builders_.has_key(b.id())

    def values(self):
        return self.builders_.values()

    def add(self, b):
        assert not self.builders_.has_key(b.id()), str(b)
        self.builders_[b.id()] = b
        pass

    def remove(self, b):
        assert self.builders_.has_key(b.id()), str(b)
        del self.builders_[b.id()]
        pass
    pass

builder_code_ = """
from libconfix.core.require import Require
from libconfix.core.require_symbol import Require_Symbol
from libconfix.core.provide import Provide
from libconfix.core.provide_symbol import Provide_Symbol
from libconfix.core.utils.error import Error
import os

def REQUIRE(require):
    if not isinstance(require, Require):
        raise Error('REQUIRE(): argument must be of type '+str(Require))
    BUILDER_.add_require(require)
    pass

def REQUIRE_SYMBOL(symbol, urgency=Require.URGENCY_IGNORE):
    if not symbol or len(symbol)==0:
        raise Error('REQUIRE_SYMBOL(): need a non-zero symbol parameter')
    if not urgency in [URGENCY_IGNORE, URGENCY_WARN, URGENCY_ERROR]:
        raise Error('REQUIRE_SYMBOL(): urgency must be one of URGENCY_IGNORE, URGENCY_WARN, URGENCY_ERROR')
    BUILDER_.add_require(Require_Symbol(
        symbol,
        found_in=["don't yet know where - concept needed"],
        urgency=urgency))
    pass

def PROVIDE(provide):
    if not isinstance(provide, Provide):
        raise Error('PROVIDE(): argument must be of type '+str(Provide)+' (was '+str(provide)+')')
    BUILDER_.add_provide(provide)
    pass

def PROVIDE_SYMBOL(symbol, match=EXACT_MATCH):
    if not symbol or len(symbol) == 0:
        raise Error('PROVIDE_SYMBOL(): need a non-zero symbol parameter')
    if not match in [EXACT_MATCH, PREFIX_MATCH, GLOB_MATCH]:
        raise Error('PROVIDE_SYMBOL(): match must be one of EXACT_MATCH, PREFIX_MATCH, GLOB_MATCH')
    BUILDER_.add_provide(Provide_Symbol(symbol=symbol, match=match))
    pass
"""
