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

from libconfix.core.filebuilder import FileBuilder
from libconfix.core.utils.error import Error
from libconfix.core.utils import helper

class PlainFileBuilder(FileBuilder):
    def __init__(self,
                 file,
                 parentbuilder,
                 package,
                 datadir=None,
                 prefixdir=None):
        assert (datadir is not None and prefixdir is None) or \
               (datadir is None and prefixdir is not None)
        FileBuilder.__init__(self,
                             file=file,
                             parentbuilder=parentbuilder,
                             package=package)
        self.datadir_ = None
        self.prefixdir_ = None
        
        if datadir is not None:        
            try:
                self.datadir_ = helper.make_path(datadir)
            except Error, e:
                raise Error('PlainFileBuilder: datadir conversion', [e])
            pass
        if prefixdir is not None:
            try:
                self.prefixdir_ = helper.make_path(prefixdir)
            except Error, e:
                raise Error('PlainFileBuilder: prefixdir conversion', [e])
            pass
        pass

    def datadir(self):
        return self.datadir_

    def prefixdir(self):
        return self.prefixdir_

    def output(self):
        FileBuilder.output(self)

        if self.datadir_ is not None:
            self.parentbuilder().file_installer().add_datafile(
                filename=self.file().name(),
                dir=self.datadir_)
        elif self.prefixdir_ is not None:
            self.parentbuilder().file_installer().add_prefixfile(
                filename=self.file().name(),
                dir=self.prefixdir_)
        else:
            assert 0
            pass
        pass

    pass
