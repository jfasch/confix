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

from linked import LinkedBuilder
from buildinfo import BuildInfo_CLibrary_NativeLocal

from libconfix.core.utils.paragraph import Paragraph, OrderedParagraphSet
from libconfix.core.automake import helper_automake

class LibraryBuilder(LinkedBuilder):
    def __init__(self,
                 parentbuilder,
                 package,
                 basename,
                 use_libtool,
                 libtool_version_info):
        LinkedBuilder.__init__(
            self,
            id=str(self.__class__)+'('+str(parentbuilder)+','+basename+')',
            parentbuilder=parentbuilder,
            package=package,
            use_libtool=use_libtool)

        self.basename_ = basename
        self.libtool_version_info_ = libtool_version_info
        
        self.add_buildinfo(BuildInfo_CLibrary_NativeLocal(
            dir=self.parentbuilder().directory().relpath(package.rootdirectory()),
            name=self.basename_))
        pass

    def basename(self):
        return self.basename_

    def libname(self):
        if self.use_libtool():
            return 'lib'+self.basename_+'.la'
        else:
            return 'lib'+self.basename_+'.a'
        pass

    def output(self):
        LinkedBuilder.output(self)

        mf_am = self.parentbuilder().makefile_am()
        am_basename = helper_automake.automake_name(self.basename())
        am_libname = helper_automake.automake_name(self.libname())

        if self.use_libtool():
            mf_am.add_ltlibrary(self.libname())
            if self.libtool_version_info_ is not None:
                mf_am.add_compound_ldflags(am_libname, '-version-info %d:%d:%d' % self.libtool_version_info_)
                pass
            pass
        else:
            self.package().configure_ac().add_paragraph(
                paragraph=Paragraph(['AC_PROG_RANLIB']),
                order=OrderedParagraphSet.PROGRAMS)
            mf_am.add_library(self.libname())
            pass
        
        for m in self.members():
            mf_am.add_compound_sources(am_libname, m.file().name())
            pass

        if self.use_libtool():
            for fragment in LinkedBuilder.get_linkline(self):
                mf_am.add_compound_libadd(
                    compound_name=am_libname,
                    lib=fragment)
                pass
            pass
        pass

    pass
