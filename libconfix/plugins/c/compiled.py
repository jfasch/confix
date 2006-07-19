# $Id: compiled.py,v 1.4 2006/07/13 20:27:24 jfasch Exp $

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
from buildinfo import BuildInfo_CIncludePath_NativeLocal

class CompiledCBuilder(CBaseBuilder):
    def __init__(self, file, parentbuilder, coordinator):
        CBaseBuilder.__init__(
            self,
            file=file,
            parentbuilder=parentbuilder,
            coordinator=coordinator)
        self.init_buildinfo_()
        pass

    def buildinfo_includepath(self):
        return self.buildinfo_includepath_

    def relate(self, node, digraph, topolist):
        CBaseBuilder.relate(self, node, digraph, topolist)
        self.init_buildinfo_()
        for n in topolist:
            for bi in n.buildinfos():
                if isinstance(bi, BuildInfo_CIncludePath_NativeLocal):
                    self.buildinfo_includepath_.insert(0, bi)
                    continue
                pass
            pass
        pass

    def init_buildinfo_(self):
        self.buildinfo_includepath_ = []
        pass
    pass

