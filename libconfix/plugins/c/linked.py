# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2008 Joerg Faschingbauer

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

from libconfix.core.digraph import algorithm
from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.filebuilder import FileBuilder

from buildinfo import \
     BuildInfo_CLibrary_NativeLocal, \
     BuildInfo_CLibrary_NativeInstalled, \
     BuildInfo_CLibrary_External

import sys

class LinkedBuilder(Builder):
    def __init__(self):
        Builder.__init__(self)

        self.__init_buildinfo()
        self.__members = set()
        pass

    def members(self):
        return self.__members

    def add_member(self, b):
        assert isinstance(b, FileBuilder)
        self.__members.add(b)
        pass

    def remove_member(self, b):
        self.__members.remove(b)
        pass

    def buildinfo_direct_dependent_native_libs(self):
        return self.__buildinfo_direct_dependent_native_libs
    def buildinfo_topo_dependent_native_libs(self):
        return self.__buildinfo_topo_dependent_native_libs
    def external_libpath(self):
        return self.__external_libpath
    def external_libraries(self):
        return self.__external_libraries

    def relate(self, node, digraph, topolist):
        Builder.relate(self, node, digraph, topolist)
        self.__init_buildinfo()

        # of the native (confix-built) libraries we remember both the
        # next successors that have a library (for libtool, which does
        # topological sorting by itself) and the toposorted list (if
        # we do not use libtool).

        # we do not know if an external library was built with
        # libtool, so we have to pass the full topolist in either
        # case.

        nodes_with_library = algorithm.nearest_property(digraph=digraph, entrypoint=node, property=HaveLibraryProperty())
        for n in nodes_with_library:
            for bi in n.buildinfos():
                if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                    self.__buildinfo_direct_dependent_native_libs.append(bi)
                    continue
                if isinstance(bi, BuildInfo_CLibrary_NativeInstalled):
                    self.__buildinfo_direct_dependent_native_libs.append(bi)
                    continue
                pass
            pass
        
        for n in topolist:
            for bi in n.buildinfos():
                if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                    self.__buildinfo_topo_dependent_native_libs.insert(0, bi)
                    continue
                if isinstance(bi, BuildInfo_CLibrary_NativeInstalled):
                    self.__buildinfo_topo_dependent_native_libs.insert(0, bi)
                    continue
                if isinstance(bi, BuildInfo_CLibrary_External):
                    key = '.'.join(bi.libpath())
                    if not key in self.__have_external_libpath:
                        self.__have_external_libpath.add(key)
                        self.__external_libpath.insert(0, bi.libpath())
                        pass
                    self.__external_libraries.insert(0, bi.libs())
                    continue
                pass
            pass
        pass

    def __init_buildinfo(self):
        self.__buildinfo_direct_dependent_native_libs = []
        self.__buildinfo_topo_dependent_native_libs = []
        self.__external_libpath = []
        self.__have_external_libpath = set()
        self.__external_libraries = []
        pass

    pass

class HaveLibraryProperty:
    def have(self, node):
        for bi in node.buildinfos():
            if isinstance(bi, BuildInfo_CLibrary_NativeLocal) or \
               isinstance(bi, BuildInfo_CLibrary_NativeInstalled) or \
               isinstance(bi, BuildInfo_CLibrary_External):
                return True
            pass
        return False
    pass
