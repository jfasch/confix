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

from libconfix.core.builder import Builder
import libconfix.core.filesys

from h import HeaderBuilder
from c import CBuilder
from cxx import CXXBuilder

class Creator(Builder):
    def __init__(self, parentbuilder, package):
        Builder.__init__(
            self,
            id=str(self.__class__)+'('+str(parentbuilder)+')',
            parentbuilder=parentbuilder,
            package=package)
        self.handled_entries_ = set()
        pass
    
    def enlarge(self):
        newbuilders = []
        for name, entry in self.parentbuilder().entries():
            if not isinstance(entry, libconfix.core.filesys.file.File):
                continue
            if entry in self.handled_entries_:
                continue
            if name.endswith('.h') or \
               name.endswith('.hh') or \
               name.endswith('.hpp'):
                newbuilders.append((entry,
                                    HeaderBuilder(file=entry,
                                                  parentbuilder=self.parentbuilder(),
                                                  package=self.package())))
                continue
            if entry.name().endswith('.c'):
                newbuilders.append((entry,
                                    CBuilder(file=entry,
                                             parentbuilder=self.parentbuilder(),
                                             package=self.package())))
                continue
            if entry.name().endswith('.cpp') or \
               entry.name().endswith('.cc') or \
               entry.name().endswith('.cxx'):
                newbuilders.append((entry,
                                    CXXBuilder(file=entry,
                                               parentbuilder=self.parentbuilder(),
                                               package=self.package())))
                continue
            pass
        for entry, b in newbuilders:
            self.parentbuilder().add_builder(b)
            self.handled_entries_.add(entry)
            pass

        return len(newbuilders) + Builder.enlarge(self)

    pass
