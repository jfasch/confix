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

from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.utils.error import Error

class DirectoryBuilderInterfaceProxy(InterfaceProxy):
    def __init__(self, directory_builder):
        InterfaceProxy.__init__(self)
        self.directory_builder_ = directory_builder
        self.add_global('IGNORE_ENTRIES', getattr(self, 'IGNORE_ENTRIES'))
        self.add_global('EXTRA_DIST', getattr(self, 'EXTRA_DIST'))
        self.add_global('MAKEFILE_AM', getattr(self, 'MAKEFILE_AM'))
        self.add_global('FILE_PROPERTIES', getattr(self, 'FILE_PROPERTIES'))
        self.add_global('FILE_PROPERTY', getattr(self, 'FILE_PROPERTY'))
        pass
    def IGNORE_ENTRIES(self, names):
        self.directory_builder_.add_ignored_entries(names)
        pass
    def EXTRA_DIST(self, filename):
        self.directory_builder_.makefile_am().add_extra_dist(filename)
        pass
    def MAKEFILE_AM(self, line):
        self.directory_builder_.makefile_am().add_line(line)
        pass

    def FILE_PROPERTIES(self, filename, properties):
        if type(properties) is not types.DictionaryType:
            raise Error('FILE_PROPERTIES(): properties parameter must be a dictionary')
        file = self.directory_builder_.directory().find([filename])
        if file is None:
            raise Error('FILE_PROPERTIES(): '
                        'file "'+filename+'" not found in directory "'+\
                        os.sep.join(self.directory_builder_.directory().relpath())+'"')
        errors = []
        for name, value in properties.iteritems():
            try:
                file.set_property(name, value)
            except Error, e:
                errors.append(e)
                pass
            pass
        if len(errors):
            raise Error('FILE_PROPERTIES('+filename+'): could not set properties', errors)
        pass

    def FILE_PROPERTY(self, filename, name, value):
        file = self.directory_builder_.directory().find([filename])
        if file is None:
            raise Error('FILE_PROPERTY(): '
                        'file "'+filename+'" not found in directory "'+\
                        os.sep.join(self.directory_builder_.directory().relpath())+'"')
        try:
            file.set_property(name, value)
        except Error, e:
            raise Error('FILE_PROPERTY('+filename+'): could not set property "'+name+'"', [e])
        pass
        
    pass
