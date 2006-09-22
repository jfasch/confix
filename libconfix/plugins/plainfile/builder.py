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

class PlainFileBuilder(FileBuilder):

    DATA = 0
    PREFIX = 1

    def __init__(self,
                 file,
                 parentbuilder,
                 package,
                 installtype,
                 installdir):
        assert installtype in [PlainFileBuilder.DATA, PlainFileBuilder.PREFIX]
        
        FileBuilder.__init__(self,
                             file=file,
                             parentbuilder=parentbuilder,
                             package=package)

        self.installtype_ = installtype
        self.installdir_ = installdir

        pass

    def output(self):
        FileBuilder.output(self)

        if self.installtype_ == PlainFileBuilder.DATA:
            self.parentbuilder().file_installer().add_datafile(filename=self.filename(), dir=self.installdir_)
        elif self.installtype_ == PlainFileBuilder.PREFIX:
            self.parentbuilder().file_installer().add_prefixfile(filename=self.filename(), dir=self.installdir_)
        else:
            assert 0
            pass
        pass

    pass
