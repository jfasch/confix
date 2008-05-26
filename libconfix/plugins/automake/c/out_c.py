# Copyright (C) 2008 Joerg Faschingbauer

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

from libconfix.plugins.automake.configure_ac import Configure_ac
from libconfix.plugins.automake import readonly_prefixes
from libconfix.plugins.automake import helper

from libconfix.plugins.c.h import HeaderBuilder
from libconfix.plugins.c.compiled import CompiledCBuilder
from libconfix.plugins.c.c import CBuilder
from libconfix.plugins.c.cxx import CXXBuilder
from libconfix.plugins.c.lex import LexBuilder
from libconfix.plugins.c.yacc import YaccBuilder
from libconfix.plugins.c.linked import LinkedBuilder
from libconfix.plugins.c.library import LibraryBuilder
from libconfix.plugins.c.executable import ExecutableBuilder
from libconfix.plugins.c.buildinfo import \
     BuildInfo_CLibrary_NativeLocal, \
     BuildInfo_CLibrary_NativeInstalled, \
     BuildInfo_CLibrary_External

from libconfix.core.utils.paragraph import Paragraph
from libconfix.core.utils import const
from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.setup import Setup

import sys
import os

class COutputSetup(Setup):
    def __init__(self, use_libtool):
        Setup.__init__(self)
        self.__use_libtool = use_libtool
        pass
    def initial_builders(self):
        return super(COutputSetup, self).initial_builders() + \
               [HeaderOutputBuilder(),
                
                CompiledOutputBuilder(),
                COutputBuilder(),
                CXXOutputBuilder(),
                LexOutputBuilder(),
                YaccOutputBuilder(),
                
                LinkedOutputBuilder(use_libtool=self.__use_libtool),
                LibraryOutputBuilder(use_libtool=self.__use_libtool),
                ExecutableOutputBuilder(use_libtool=self.__use_libtool)
                ]
    pass

class HeaderOutputBuilder(Builder):
    def locally_unique_id(self):
        return str(self.__class__)
    def output(self):
        super(HeaderOutputBuilder, self).output()
        for b in self.parentbuilder().builders():
            if not isinstance(b, HeaderBuilder):
                continue

            public_visibility = b.public_visibility()
            local_visibility = b.local_visibility()

            self.parentbuilder().file_installer().add_public_header(filename=b.file().name(), dir=public_visibility)

            assert local_visibility[0] in (HeaderBuilder.LOCAL_INSTALL, HeaderBuilder.DIRECT_INCLUDE)
            if local_visibility[0] == HeaderBuilder.LOCAL_INSTALL:
                self.parentbuilder().file_installer().add_private_header(
                    filename=b.file().name(),
                    dir=local_visibility[1])
                pass
            pass
        pass
    pass

class CompiledOutputBuilder(Builder):
    def locally_unique_id(self):
        return str(self.__class__)
    def output(self):
        super(CompiledOutputBuilder, self).output()
        for b in self.parentbuilder().builders():
            if not isinstance(b, CompiledCBuilder):
                continue

            for name, value in b.cmdlinemacros().iteritems():
                self.parentbuilder().makefile_am().add_cmdlinemacro(name, value)
                pass
            for f in b.cflags():
                self.parentbuilder().makefile_am().add_am_cflags(f)
                pass
    
            # native includes of the same package come first
            for d in b.native_local_include_dirs():
                self.parentbuilder().makefile_am().add_includepath('-I'+'/'.join(['$(top_srcdir)']+d))
                pass
            # if files have been locally installed, we have to add
            # $(top_builddir)/confix_include to the include path.
            if b.have_locally_installed_includes():
                self.parentbuilder().makefile_am().add_includepath('-I'+'/'.join(['$(top_builddir)', const.LOCAL_INCLUDE_DIR]))
                pass
            # native includes of other packages (i.e., native installed
            # includes) come next.
            if b.using_native_installed():
                self.parentbuilder().makefile_am().add_includepath('-I$(includedir)')
                self.parentbuilder().makefile_am().add_includepath('$('+readonly_prefixes.incpath_var+')')
                pass
            # external includes.
            for p in b.external_include_path():
                for item in p:
                    self.parentbuilder().makefile_am().add_includepath(item)
                    pass
                pass
            pass
        pass
    pass

class COutputBuilder(Builder):
    def locally_unique_id(self):
        return str(self.__class__)
    def output(self):
        super(COutputBuilder, self).output()
        for b in self.parentbuilder().builders():
            if not isinstance(b, CBuilder):
                continue

            self.package().configure_ac().add_paragraph(
                paragraph=Paragraph(['AC_PROG_CC']),
                order=Configure_ac.PROGRAMS)
            pass
        pass
    pass

class CXXOutputBuilder(Builder):
    def locally_unique_id(self):
        return str(self.__class__)
    def output(self):
        super(CXXOutputBuilder, self).output()
        for b in self.parentbuilder().builders():
            if not isinstance(b, CXXBuilder):
                continue

            self.package().configure_ac().add_paragraph(
                paragraph=Paragraph(['AC_PROG_CXX']),
                order=Configure_ac.PROGRAMS)
            for f in b.cxxflags():
                self.parentbuilder().makefile_am().add_am_cxxflags(f)
                pass
            pass
        pass
    pass

class LexOutputBuilder(Builder):
    def locally_unique_id(self):
        return str(self.__class__)
    def output(self):
        super(LexOutputBuilder, self).output()
        for b in self.parentbuilder().builders():
            if not isinstance(b, LexBuilder):
                continue

            self.package().configure_ac().add_paragraph(
                paragraph=Paragraph(['AC_PROG_LEX']),
                order=Configure_ac.PROGRAMS)
            root, ext = os.path.splitext(b.file().name())
            if ext == '.l':
                self.package().configure_ac().add_paragraph(
                    paragraph=Paragraph(['AC_PROG_CC']),
                    order=Configure_ac.PROGRAMS)
                self.parentbuilder().makefile_am().add_built_sources(root + '.c')
            elif ext == '.ll':
                self.package().configure_ac().add_paragraph(
                    paragraph=Paragraph(['AC_PROG_CXX']),
                    order=Configure_ac.PROGRAMS)
                self.parentbuilder().makefile_am().add_built_sources(root + '.cc')
                # argh: when using "%option c++" in the lex source file,
                # flex generates lex.yy.cc, which automake doesn't seem to
                # be aware of. force it to generate the file automake is
                # aware of. this is not supposed to work with other lexers
                # however. but, as the documentation states, it is better
                # to not use the C++ feature of lex since it is inherently
                # non-portable anyway.
                self.parentbuilder().makefile_am().add_am_lflags('-olex.yy.c')
            else:
                assert 0
                pass
            pass
        pass
    pass

class YaccOutputBuilder(Builder):
    def locally_unique_id(self):
        return str(self.__class__)
    def output(self):
        super(YaccOutputBuilder, self).output()
        for b in self.parentbuilder().builders():
            if not isinstance(b, YaccBuilder):
                continue

            self.package().configure_ac().add_paragraph(
                paragraph=Paragraph(['AC_PROG_YACC']),
                order=Configure_ac.PROGRAMS)
            root, ext = os.path.splitext(b.file().name())
            if ext == '.y':
                self.package().configure_ac().add_paragraph(
                    paragraph=Paragraph(['AC_PROG_CC']),
                    order=Configure_ac.PROGRAMS)
                self.parentbuilder().makefile_am().add_built_sources(root + '.c')
            elif ext == '.yy':
                self.package().configure_ac().add_paragraph(
                    paragraph=Paragraph(['AC_PROG_CXX']),
                    order=Configure_ac.PROGRAMS)
                self.parentbuilder().makefile_am().add_built_sources(root + '.cc')
                # force Yacc to output files named y.tab.h
                self.parentbuilder().makefile_am().add_am_yflags('-d');
            else:
                assert 0
                pass
            pass
        pass
    pass

class LinkedOutputBuilder(Builder):
    def __init__(self, use_libtool):
        Builder.__init__(self)
        self.__use_libtool = use_libtool
        pass
    def locally_unique_id(self):
        return str(self.__class__)
    def output(self):
        super(LinkedOutputBuilder, self).output()
        for b in self.parentbuilder().builders():
            if not isinstance(b, LinkedBuilder):
                continue

            if self.__use_libtool:
                self.package().configure_ac().add_paragraph(
                    paragraph=Paragraph(['AC_LIBTOOL_DLOPEN',
                                         'AC_LIBTOOL_WIN32_DLL',
                                         'AC_PROG_LIBTOOL']),
                    order=Configure_ac.PROGRAMS)
                pass
            pass
        pass
    pass

class LibraryOutputBuilder(Builder):
    def __init__(self, use_libtool):
        Builder.__init__(self)
        self.__use_libtool = use_libtool
        pass
    def locally_unique_id(self):
        return str(self.__class__)
    def output(self):
        super(LibraryOutputBuilder, self).output()
        for b in self.parentbuilder().builders():
            if not isinstance(b, LibraryBuilder):
                continue

            if self.__use_libtool:
                filelibname = 'lib'+b.basename()+'.la'
            else:
                filelibname = 'lib'+b.basename()+'.a'
                pass
            automakelibname = helper.automake_name(filelibname)

            mf_am = self.parentbuilder().makefile_am()

            if self.__use_libtool:
                mf_am.add_ltlibrary(filelibname)
                if b.libtool_version_info() is not None:
                    mf_am.add_compound_ldflags(automakelibname, '-version-info %d:%d:%d' % b.libtool_version_info())
                elif b.libtool_release_info() is not None:
                    mf_am.add_compound_ldflags(automakelibname, '-release '+b.libtool_release_info())
                    pass
                pass
            else:
                self.package().configure_ac().add_paragraph(
                    paragraph=Paragraph(['AC_PROG_RANLIB']),
                    order=Configure_ac.PROGRAMS)
                mf_am.add_library(filelibname)
                pass

            for m in b.members():
                mf_am.add_compound_sources(automakelibname, m.file().name())
                pass

            if self.__use_libtool:
                for fragment in _linked_get_linkline(builder=b, use_libtool=self.__use_libtool):
                    mf_am.add_compound_libadd(
                        compound_name=automakelibname,
                        lib=fragment)
                    pass
                pass
            pass
        pass
    pass

class ExecutableOutputBuilder(Builder):
    def __init__(self, use_libtool):
        Builder.__init__(self)
        self.__use_libtool = use_libtool
        pass
    def locally_unique_id(self):
        return str(self.__class__)
    def output(self):
        super(ExecutableOutputBuilder, self).output()
        for b in self.parentbuilder().builders():
            if not isinstance(b, ExecutableBuilder):
                continue

            mf_am = self.parentbuilder().makefile_am()

            if b.what() == ExecutableBuilder.BIN:
                mf_am.add_bin_program(b.exename())
            elif b.what() == ExecutableBuilder.CHECK:
                mf_am.add_check_program(b.exename())
            elif b.what() == ExecutableBuilder.NOINST:
                mf_am.add_noinst_program(b.exename())
            else: assert 0

            automakeexename = helper.automake_name(b.exename())

            for m in b.members():
                mf_am.add_compound_sources(automakeexename, m.file().name())
                pass

            for fragment in _linked_get_linkline(builder=b, use_libtool=self.__use_libtool):
                mf_am.add_compound_ldadd(
                    compound_name=automakeexename,
                    lib=fragment)
                pass
            pass
        pass
    pass

def _linked_get_linkline(builder, use_libtool):
    """
    Returns a list of strings, like ['-L/blah -L/bloh/blah
    -lonelibrary -lanotherone']
    """
    native_paths = []
    native_libraries = []
    external_linkline = []
    using_installed_library = False

    if _linked_do_deep_linking(use_libtool=use_libtool):
        native_libs_to_use = builder.buildinfo_topo_dependent_native_libs()
    else:
        native_libs_to_use = builder.buildinfo_direct_dependent_native_libs()
        pass

    for bi in native_libs_to_use:
        if isinstance(bi, BuildInfo_CLibrary_NativeLocal):
            native_paths.append('-L'+'/'.join(['$(top_builddir)']+bi.dir()))
            native_libraries.append('-l'+bi.name())
            continue
        if isinstance(bi, BuildInfo_CLibrary_NativeInstalled):
            using_installed_library = True
            native_libraries.append('-l'+bi.name())
            continue
        assert 0
        pass

    if using_installed_library:
        native_paths.append('-L$(libdir)')
        native_paths.append('$('+readonly_prefixes.libpath_var+')')
        pass

    # in either case (libtool or not), we have to link all external
    # libraries. we cannot decide whether they are built with libtool
    # or not, so we cannot rely on libtool making our toposort. (note
    # both are lists of lists...)
    for elem in builder.external_libpath() + builder.external_libraries():
        external_linkline.extend(elem)
        pass

    return native_paths + native_libraries + external_linkline

def _linked_do_deep_linking(use_libtool):
    """
    Returns a boolean value indicating if deep linking is desired or
    not. 'Deep linking' means that the whole dependency graph is
    reflected on the command line, in a topologically sorted way. As
    opposed to flat linking (or how one calls it), where only the
    direct dependent libraries are mentioned.
    """
    if use_libtool:
        if not sys.platform.startswith('interix'):
            # when linking anything with libtool, we don't need to
            # specify the whole topologically sorted list of
            # dependencies - libtool does that by itself (*). We only
            # specify the direct dependencies.

            # (*) It is still unclear to me what the Libtool policy
            # is. I suspect it relies on the fact that the native
            # linker permits unresolved references (GNU ld is happy
            # with them, at the very least).
            return False
        else:
            # on Interix, Parity
            # (http://sourceforge.net/projects/parity) does things in
            # a way that the Windows native linker is invoked. That
            # guy likes things rather explicit, and is very particular
            # about unresolved references:
            return True
        pass
    else:
        # not using libtool; doing a dumb static link.
        return True
    pass

