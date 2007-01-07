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

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.iface.code_piece import CodePiece
from libconfix.core.iface.executor import InterfaceExecutor
from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.filebuilder import FileBuilder
from libconfix.core.machinery.setup import Setup

class FileInterfaceTestSetup(Setup):
    def __init__(self):
        Setup.__init__(self)
        pass
    def initial_builders(self):
        ret = super(FileInterfaceTestSetup, self).initial_builders()
        ret.add_builder(FileInterfaceTestCreator())
        return ret
    pass

class FileInterfaceTestCreator(Builder):
    def __init__(self):
        Builder.__init__(self)
        self.handled_entries_ = set()
        pass

    def locally_unique_id(self):
        return str(self.__class__)

    def enlarge(self):
        super(FileInterfaceTestCreator, self).enlarge()
        for name, entry in self.parentbuilder().entries():
            if not isinstance(entry, File):
                continue
            if entry in self.handled_entries_:
                continue
            if name.endswith('.iface'):
                self.parentbuilder().add_builder(FileInterfaceTestBuilder(file=entry))
                self.handled_entries_.add(entry)
                continue
            pass
        pass
    pass

class FileInterfaceTestBuilder(FileBuilder):
    def __init__(self, file):
        FileBuilder.__init__(self, file=file)
        lines=file.lines()
        if len(lines):
            execer = InterfaceExecutor(iface_pieces=self.iface_pieces())
            execer.execute_pieces([CodePiece(start_lineno=1, lines=lines)])
            pass

        self.node_ = None
        self.topolist_ = None
        self.successors_ = None
        self.relate_calls_ = 0
        self.enlarge_calls_ = 0
        pass
    def node(self):
        return self.node_
    def topolist(self):
        return self.topolist_
    def successors(self):
        return self.successors_
    def enlarge(self):
        self.enlarge_calls_ += 1
        return FileBuilder.enlarge(self)
    def relate(self, node, digraph, topolist):
        FileBuilder.relate(self, node, digraph, topolist)
        self.node_ = node
        self.topolist_ = topolist
        self.successors_ = digraph.successors(node)
        self.relate_calls_ += 1
        pass
    def iface_pieces(self):
        return FileBuilder.iface_pieces(self)
    def relate_calls(self):
        return self.relate_calls_
    def enlarge_calls(self):
        return self.enlarge_calls_
    pass
