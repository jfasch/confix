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

from libconfix.plugins.c.h import HeaderBuilder
from libconfix.plugins.automake.configure_ac import Configure_ac
from libconfix.core.machinery.builder import Builder

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
        super(HeaderOutputBuilder, self).output()
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
        for p in b.get_includepath():
            self.parentbuilder().makefile_am().add_includepath(p)
            pass
        for name, value in b.get_cmdlinemacros():
            self.parentbuilder().makefile_am().add_cmdlinemacro(name, value)
            pass
        for f in b.get_cflags():
            self.parentbuilder().makefile_am().add_am_cflags(f)
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
        

    pass
