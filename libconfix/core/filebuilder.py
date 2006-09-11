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

from entrybuilder import EntryBuilder

from iface import InterfacePiece

class FileBuilder(EntryBuilder):
    def __init__(self, file, parentbuilder, package):
        EntryBuilder.__init__(self,
                              id=str(self.__class__)+'('+'/'.join(file.relpath(package.rootdirectory()))+')',
                              entry=file,
                              parentbuilder=parentbuilder,
                              package=package)
        pass
    def file(self):
        return self.entry()
    def iface_pieces(self):
        return EntryBuilder.iface_pieces(self) + \
               [InterfacePiece(globals={'ENTRY_': self.file()},
                               lines=[iface])]
    pass

iface = """
from libconfix.core.utils.error import Error

import types

def FILE_PROPERTIES(properties, filename=None):
    global ENTRY_
    if properties is None:
        raise Error("FILE_PROPERTIES(): 'properties' parameter cannot be None")
    if not type(properties) is types.DictionaryType:
        raise Error("FILE_PROPERTIES(): 'properties' parameter must be a dictionary")
    file = find_file(filename)
    for name, value in properties.iteritems():
        file.set_property(name=name, value=value)
        pass
    pass

def FILE_PROPERTY(name, value, filename=None):
    global ENTRY_
    if type(name) is not types.StringType:
        raise Error("FILE_PROPERTY(): 'name' must be a string")
    file = find_file(filename)
    file.set_property(name, value)
    pass

def find_file(filename):
    if filename is None:
        file = ENTRY_
    else:
        file = ENTRY_.parent().get(filename)
        if file is None:
            raise Error('FILE_PROPERTIES(): file '+filename+' not found in directory '+ENTRY_.parent().name())
        pass
    return file
"""
