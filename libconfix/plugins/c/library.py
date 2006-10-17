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

import types

from libconfix.core.utils.paragraph import Paragraph, OrderedParagraphSet
from libconfix.core.automake import helper_automake
from libconfix.core.automake.configure_ac import Configure_ac

from linked import LinkedBuilder
from buildinfo import BuildInfo_CLibrary_NativeLocal

class LibraryBuilder(LinkedBuilder):
    def __init__(self,
                 parentbuilder,
                 package,
                 basename,
                 use_libtool,
                 libtool_version_info,
                 libtool_release_info):

        # libtool version information; to be passed to libtool
        # -version-info <current>:<revision>:<age>
        assert libtool_version_info is None or \
               type(libtool_version_info) in [types.ListType, types.TupleType] and len(libtool_version_info) == 3

        # libtool release information; to be passed as -release
        # <package-version>
        assert libtool_release_info is None or \
               type(libtool_release_info) is types.StringType
        
        LinkedBuilder.__init__(
            self,
            id=str(self.__class__)+'('+str(parentbuilder)+','+basename+')',
            parentbuilder=parentbuilder,
            package=package,
            use_libtool=use_libtool)

        self.__basename = basename
        self.__libtool_version_info = libtool_version_info
        self.__libtool_release_info = libtool_release_info
        
        self.add_buildinfo(BuildInfo_CLibrary_NativeLocal(
            dir=self.parentbuilder().directory().relpath(package.rootdirectory()),
            name=self.__basename))
        pass

    def basename(self):
        return self.__basename

    def libname(self):
        if self.use_libtool():
            return 'lib'+self.__basename+'.la'
        else:
            return 'lib'+self.__basename+'.a'
        pass

    def libtool_version_info(self):
        return self.__libtool_version_info

    def libtool_release_info(self):
        return self.__libtool_release_info

    def output(self):
        LinkedBuilder.output(self)

        mf_am = self.parentbuilder().makefile_am()
        am_basename = helper_automake.automake_name(self.basename())
        am_libname = helper_automake.automake_name(self.libname())

        if self.use_libtool():
            mf_am.add_ltlibrary(self.libname())
            if self.__libtool_version_info is not None:
                mf_am.add_compound_ldflags(am_libname, '-version-info %d:%d:%d' % self.__libtool_version_info)
            elif self.__libtool_release_info is not None:
                mf_am.add_compound_ldflags(am_libname, '-release '+self.__libtool_release_info)
                pass
            pass
        else:
            self.package().configure_ac().add_paragraph(
                paragraph=Paragraph(['AC_PROG_RANLIB']),
                order=Configure_ac.PROGRAMS)
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
