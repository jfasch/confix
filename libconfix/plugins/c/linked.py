# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006 Joerg Faschingbauer

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

from libconfix.core.utils.paragraph import Paragraph, OrderedParagraphSet
from libconfix.core.filebuilder import FileBuilder
from libconfix.core.builder import Builder, BuilderSet
from libconfix.core.automake.configure_ac import Configure_ac
from libconfix.core import readonly_prefixes

from buildinfo import \
     BuildInfo_CLibrary_NativeLocal, \
     BuildInfo_CLibrary_NativeInstalled, \
     BuildInfo_CLibrary_External

class LinkedBuilder(Builder):
    def __init__(self, id, parentbuilder, package, use_libtool):
        Builder.__init__(
            self,
            id=id,
            parentbuilder=parentbuilder,
            package=package)

        self.__init_buildinfo()
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
    
    def buildinfo_direct_dependent_native_libs(self):
        return self.buildinfo_direct_dependent_native_libs_
    def buildinfo_topo_dependent_native_libs(self):
        return self.buildinfo_topo_dependent_native_libs_
    def external_libpath(self):
        return self.external_libpath_
    def external_libraries(self):
        return self.external_libraries_

    def relate(self, node, digraph, topolist):
        Builder.relate(self, node, digraph, topolist)
        self.__init_buildinfo()

        # of the native (confix-built) libraries we remember both the
        # direct successors (for libtool, which does topological
        # sorting by itself) and the toposorted list (if we do not use
        # libtool).

        # we do not know if an external library was built with
        # libtool, so we have to pass the full topolist in either
        # case.
        
        for n in digraph.successors(node):
            for bi in n.buildinfos():
                if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                    self.buildinfo_direct_dependent_native_libs_.append(bi)
                    continue
                if isinstance(bi, BuildInfo_CLibrary_NativeInstalled):
                    self.buildinfo_direct_dependent_native_libs_.append(bi)
                    continue
                pass
            pass
        for n in topolist:
            for bi in n.buildinfos():
                if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                    self.buildinfo_topo_dependent_native_libs_.insert(0, bi)
                    continue
                if isinstance(bi, BuildInfo_CLibrary_NativeInstalled):
                    self.buildinfo_topo_dependent_native_libs_.insert(0, bi)
                    continue
                if isinstance(bi, BuildInfo_CLibrary_External):
                    key = '.'.join(bi.libpath())
                    if not key in self.have_external_libpath_:
                        self.have_external_libpath_.add(key)
                        self.external_libpath_.insert(0, bi.libpath())
                        pass
                    self.external_libraries_.insert(0, bi.libs())
                    continue
                pass
            pass
        pass

    def output(self):
        Builder.output(self)
        if self.use_libtool_:
            self.package().configure_ac().add_paragraph(
                paragraph=Paragraph(['AC_LIBTOOL_DLOPEN',
                                     'AC_LIBTOOL_WIN32_DLL',
                                     'AC_PROG_LIBTOOL']),
                order=Configure_ac.PROGRAMS)
            pass
        pass

    def get_linkline(self):
        paths = []
        libraries = []
        using_installed_library = False

        if self.use_libtool_:
            # when linking anything with libtool, we don't need to
            # specify the whole topologically sorted list of
            # dependencies - libtool does that by itself. we only
            # specify the direct dependencies.
            libs_to_use = self.buildinfo_direct_dependent_native_libs_
        else:
            # not using libtool; have to toposort ourselves
            libs_to_use = self.buildinfo_topo_dependent_native_libs_
            pass

        for bi in libs_to_use:
            if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
                paths.append('-L'+'/'.join(['$(top_builddir)']+bi.dir()))
                libraries.append('-l'+bi.name())
                continue
            if isinstance(bi, BuildInfo_CLibrary_NativeInstalled):
                using_installed_library = True
                libraries.append('-l'+bi.name())
                continue
            assert 0
            pass

        if using_installed_library:
            paths.append('-L$(libdir)')
            paths.append(readonly_prefixes.libpath_subst)
            pass

        return paths + libraries
    
    def __init_buildinfo(self):
        self.buildinfo_direct_dependent_native_libs_ = []
        self.buildinfo_topo_dependent_native_libs_ = []
        self.external_libpath_ = []
        self.have_external_libpath_ = set()
        self.external_libraries_ = []
        pass

    pass
