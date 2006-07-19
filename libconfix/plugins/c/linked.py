# $Id: linked.py,v 1.2 2006/07/13 20:27:24 jfasch Exp $

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

from buildinfo import BuildInfo_CLibrary_NativeLocal

from libconfix.core.filebuilder import FileBuilder
from libconfix.core.builder import Builder, BuilderSet

class LinkedBuilder(Builder):
    def __init__(self, id, parentbuilder, coordinator, use_libtool):
        Builder.__init__(
            self,
            id=id,
            parentbuilder=parentbuilder,
            coordinator=coordinator)

        self.init_buildinfo_()
        self.members_ = BuilderSet()
        self.use_libtool_ = use_libtool
        pass

    def members(self):
        return self.members_

    def add_member(self, b):
        assert isinstance(b, FileBuilder)
        self.members_.add(b)
        pass

    def use_libtool(self):
        return self.use_libtool_

    def buildinfo_direct_dependent_libs(self):
        return self.buildinfo_direct_dependent_libs_
    def buildinfo_topo_dependent_libs(self):
        return self.buildinfo_topo_dependent_libs_

    def relate(self, node, digraph, topolist):
        Builder.relate(self, node, digraph, topolist)
        self.init_buildinfo_()
        for n in digraph.successors(node):
            for bi in n.buildinfos():
                if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                    self.buildinfo_direct_dependent_libs_.append(bi)
                    continue
                pass
            pass
        for n in topolist:
            for bi in n.buildinfos():
                if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                    self.buildinfo_topo_dependent_libs_.insert(0, bi)
                    continue
                pass
            pass
                
        pass

    def init_buildinfo_(self):
        self.buildinfo_direct_dependent_libs_ = []
        self.buildinfo_topo_dependent_libs_ = []
        pass

    pass
