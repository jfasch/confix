# $Id: library.py,v 1.8 2006/07/13 20:27:24 jfasch Exp $

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
from buildinfo import BuildInfo_CIncludePath_NativeLocal, BuildInfo_CLibrary_NativeLocal

from libconfix.core.automake import helper_automake, helper_optmod

class LibraryBuilder(LinkedBuilder):
    def __init__(self,
                 parentbuilder,
                 coordinator,
                 basename,
                 use_libtool,
                 libtool_version_info):
        LinkedBuilder.__init__(
            self,
            id=str(self.__class__)+'('+str(parentbuilder)+','+basename+')',
            parentbuilder=parentbuilder,
            coordinator=coordinator,
            use_libtool=use_libtool)

        self.basename_ = basename
        self.libtool_version_info_ = libtool_version_info
        
        self.add_buildinfo(BuildInfo_CIncludePath_NativeLocal())
        self.add_buildinfo(BuildInfo_CLibrary_NativeLocal(dir=self.parentbuilder().directory().relpath(),
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
        mf_am = self.parentbuilder().makefile_am()
        am_basename = helper_automake.automake_name(self.basename())
        am_libname = helper_automake.automake_name(self.libname())

        for m in self.members():
            mf_am.add_compound_sources(am_libname, m.file().name())
            pass

        if self.use_libtool():
            mf_am.add_ltlibrary(self.libname())
            if self.libtool_version_info_ is not None:
                mf_am.add_compound_ldflags(am_libname, '-version-info %d:%d:%d' % self.libtool_version_info_)
                pass
            for bi in self.buildinfo_direct_dependent_libs():
                mf_am.add_compound_libadd(am_libname, '/'.join(['$(top_builddir)']+bi.dir()+['lib'+bi.name()+'.la']))
                pass
            pass
        else:
            mf_am.add_library(self.libname())
            pass
        pass

    pass
