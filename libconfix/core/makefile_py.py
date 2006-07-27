# $Id: makefile_py.py,v 1.7 2006/07/07 15:29:19 jfasch Exp $

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

from filebuilder import FileBuilder
from iface import InterfaceExecutor, InterfacePiece
from libconfix.core.utils.error import Error

class Makefile_py(FileBuilder):
    def __init__(self, file, parentbuilder, package):
        FileBuilder.__init__(self,
                             file=file,
                             parentbuilder=parentbuilder,
                             package=package)
        self.executed_ = False
        pass

    def iface_pieces(self):
        return FileBuilder.iface_pieces(self) + [InterfacePiece(globals={'MAKEFILE_PY_': self},
                                                                lines=[code_])]

    def enlarge(self):
        FileBuilder.enlarge(self)
        
        if self.executed_:
            return 0
        self.executed_ = True
        try:
            iface_pieces = self.iface_pieces() + self.makefile_py_iface_pieces()
            for b in self.parentbuilder().setups():
                iface_pieces.extend(b.makefile_py_iface_pieces())
                pass
            execer = InterfaceExecutor(iface_pieces=iface_pieces)
            execer.execute_file(file=self.file())
            return 1
        except Error, e:
            raise Error('could not execute code', [e])
        pass

    def output(self):
        self.parentbuilder().makefile_am().add_extra_dist(self.file().name())
        pass
    
    pass

code_ = """
def IGNORE_ENTRIES(names):
    MAKEFILE_PY_.parentbuilder().add_ignored_entries(names)
    pass
"""
