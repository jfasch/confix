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

from filebuilder import FileBuilder
from iface import InterfaceExecutor, InterfacePiece
from libconfix.core.utils.error import Error

import os

class Confix2_in(FileBuilder):
    def __init__(self, file, parentbuilder, package):
        FileBuilder.__init__(self,
                             file=file,
                             parentbuilder=parentbuilder,
                             package=package)
        self.executed_ = False
        pass

    def iface_pieces(self):
        return FileBuilder.iface_pieces(self) + [InterfacePiece(globals={'CONFIX2_IN_': self},
                                                                lines=[code_])]

    def enlarge(self):
        FileBuilder.enlarge(self)
        
        if self.executed_:
            return 0
        self.executed_ = True
        try:
            iface_pieces = self.iface_pieces() + self.confix2_in_iface_pieces()
            for b in self.parentbuilder().setups():
                iface_pieces.extend(b.confix2_in_iface_pieces())
                pass
            execer = InterfaceExecutor(iface_pieces=iface_pieces)
            execer.execute_file(file=self.file())
            return 1
        except Error, e:
            raise Error('Could not execute file "'+\
                        os.sep.join(self.file().relpath(self.package().rootdirectory()))+'"', [e])
        pass

    def output(self):
        FileBuilder.output(self)
        self.parentbuilder().makefile_am().add_extra_dist(self.file().name())
        pass
    
    pass

code_ = """
def IGNORE_ENTRIES(names):
    CONFIX2_IN_.parentbuilder().add_ignored_entries(names)
    pass
"""
