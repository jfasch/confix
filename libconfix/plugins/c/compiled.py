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

from base import CBaseBuilder
from buildinfo import BuildInfo_CIncludePath_NativeLocal, BuildInfo_CIncludePath_NativeInstalled

from libconfix.core.utils import const

class CompiledCBuilder(CBaseBuilder):
    def __init__(self, file, parentbuilder, package):
        CBaseBuilder.__init__(
            self,
            file=file,
            parentbuilder=parentbuilder,
            package=package)
        self.init_buildinfo_()
        pass

    def buildinfo_includepath_native_local(self):
        return self.buildinfo_includepath_native_local_

    def buildinfo_includepath_native_installed(self):
        return self.buildinfo_includepath_native_installed_

    def relate(self, node, digraph, topolist):
        CBaseBuilder.relate(self, node, digraph, topolist)
        self.init_buildinfo_()
        for n in topolist:
            for bi in n.buildinfos():
                if isinstance(bi, BuildInfo_CIncludePath_NativeLocal):
                    self.buildinfo_includepath_native_local_ += 1
                    continue
                if isinstance(bi, BuildInfo_CIncludePath_NativeInstalled):
                    self.buildinfo_includepath_native_installed_ += 1
                    continue
                pass
            pass
        pass

    def output(self):
        CBaseBuilder.output(self)
        if self.buildinfo_includepath_native_local_ > 0:
            self.parentbuilder().makefile_am().add_includepath(
                '-I$(top_builddir)/'+const.LOCAL_INCLUDE_DIR)
            pass
        if self.buildinfo_includepath_native_installed_ > 0:
            self.parentbuilder().makefile_am().add_includepath(
                '-I$(includedir)')
        pass

    def init_buildinfo_(self):
        self.buildinfo_includepath_native_local_ = 0
        self.buildinfo_includepath_native_installed_ = 0
        pass
    pass

