# $Id: executable.py,v 1.5 2006/07/13 20:27:24 jfasch Exp $

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
from libconfix.core.builder import BuilderSet

class ExecutableBuilder(LinkedBuilder):
    def __init__(self, parentbuilder, package, center, exename, use_libtool):
        LinkedBuilder.__init__(
            self,
            id=str(self.__class__)+':'+str(center)+'('+str(parentbuilder)+')',
            parentbuilder=parentbuilder,
            package=package,
            use_libtool=use_libtool)

        LinkedBuilder.add_member(self, center)

        self.center_ = center
        self.exename_ = exename
        pass

    def center(self):
        return self.center_

    def output(self):
        mf_am = self.parentbuilder().makefile_am()
        mf_am.add_bin_program(self.exename_)
        for m in self.members():
            mf_am.add_compound_sources(self.exename_, m.file().name())
            pass
        if self.use_libtool():
            for bi in self.buildinfo_direct_dependent_libs():
                mf_am.add_compound_ldadd(self.exename_,
                                         '/'.join(['$(top_builddir)']+bi.dir()+['lib'+bi.name()+'.la']))
                pass
            pass
        else:
            for bi in self.buildinfo_topo_dependent_libs():
                mf_am.add_compound_ldadd(self.exename_,
                                         '/'.join(['$(top_builddir)']+bi.dir()+['lib'+bi.name()+'.a']))
                pass
            pass
        pass
        
    pass
