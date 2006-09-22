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
from libconfix.core.filesys.file import File

from builder import PlainFileBuilder

class PLAINFILE_InterfaceProxy(InterfaceProxy):
    def __init__(self, object):
        InterfaceProxy.__init__(self)
        self.object_ = object
        self.add_global('PLAINFILE_DATA', PlainFileBuilder.DATA)
        self.add_global('PLAINFILE_PREFIX', PlainFileBuilder.PREFIX)
        self.add_global('PLAINFILE', getattr(self, 'PLAINFILE'))
        pass

    def PLAINFILE(self, filename, installtype, installdir):
        if type(filename) is not types.StringType:
            raise Error('PLAINFILE(): filename must be a string')
        if installtype not in [PlainFileBuilder.DATA, PlainFileBuilder.PREFIX]:
            raise Error('PLAINFILE(): installtype must be one of PLAINFILE_DATA or PLAINFILE_PREFIX')
        if type(installdir) is not types.StringType:
            raise Error('PLAINFILE(): installdir must be a string')

        file = self.object_.directory().find([filename])
        if file is None:
            raise Error('PLAINFILE('+filename+'): no such file or directory')
        if not isinstance(file, File):
            raise Error('PLAINFILE('+filename+'): not a file')

        self.object_.add_builder(
            PlainFileBuilder(file=file,
                             parentbuilder=self.object_.parentbuilder(),
                             package=self.object_.package(),
                             installtype=installtype,
                             installdir=installdir))
        pass
