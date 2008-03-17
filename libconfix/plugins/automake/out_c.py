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

from configure_ac import Configure_ac
import readonly_prefixes

from libconfix.core.utils.paragraph import Paragraph
from libconfix.core.utils import const
from libconfix.core.machinery.builder import Builder
from libconfix.plugins.c.h import HeaderBuilder
from libconfix.plugins.c.c import CBuilder
from libconfix.plugins.c.cxx import CXXBuilder
from libconfix.plugins.c.lex import LexBuilder
from libconfix.plugins.c.yacc import YaccBuilder

class COutputBuilder(Builder):
    """
    Generate output for all of the builders of the C plugin.
    """
    
    def __init__(self):
        Builder.__init__(self)
        pass

    def locally_unique_id(self):
        # I am supposed to the only one of my kind among all the
        # builders in a directory, so my class suffices as a unique
        # id.
        return str(self.__class__)

    def output(self):
        super(COutputBuilder, self).output()
        for b in self.parentbuilder().builders():
            if isinstance(b, HeaderBuilder):
                self.__do_header(b)
                continue
            if isinstance(b, CBuilder):
                self.__do_c(b)
                continue
            if isinstance(b, CXXBuilder):
                self.__do_cxx(b)
                continue
            if isinstance(b, LexBuilder):
                self.__do_lex(b)
                continue
            if isinstance(b, YaccBuilder):
                self.__do_yacc(b)
                continue
            pass
        pass

    def __do_header(self, b):
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

    def __do_compiled(self, b):
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
            self.parentbuilder().makefile_am().add_includepath(p)
            pass
        pass

    def __do_c(self, b):
        self.__do_compiled(b)
        self.package().configure_ac().add_paragraph(
            paragraph=Paragraph(['AC_PROG_CC']),
            order=Configure_ac.PROGRAMS)
        pass

    def __do_cxx(self, b):
        self.__do_compiled(b)
        self.package().configure_ac().add_paragraph(
            paragraph=Paragraph(['AC_PROG_CXX']),
            order=Configure_ac.PROGRAMS)
        for f in b.cxxflags():
            self.parentbuilder().makefile_am().add_am_cxxflags(f)
            pass
        pass

    def __do_lex(self, b):
        self.__do_compiled(b)
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

    def __do_yacc(self, b):
        self.__do_compiled(b)
        self.package().configure_ac().add_paragraph(
            paragraph=Paragraph(['AC_PROG_YACC']),
            order=Configure_ac.PROGRAMS)
        root, ext = os.path.splitext(self.file().name())
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
