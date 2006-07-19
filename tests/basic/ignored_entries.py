# $Id: ignored_entries.py,v 1.7 2006/06/23 08:14:35 jfasch Exp $

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

from libconfix.core.builder import Builder
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.coordinator import BuildCoordinator
from libconfix.testutils import dirhier

import unittest

class FileWatcher(Builder):
    def __init__(self, parentbuilder, coordinator):
        Builder.__init__(
            self,
            id=str(self.__class__)+'('+str(parentbuilder)+')',
            parentbuilder=parentbuilder,
            coordinator=coordinator)
        self.seen_names_ = set()
        pass

    def seen_names(self):
        return self.seen_names_

    def enlarge(self):
        for name, entry in self.parentbuilder().entries():
            self.seen_names_.add(name)
            pass
        return Builder.enlarge(self)
    pass

class IgnoredEntries(unittest.TestCase):

    def test(self):
        fs = FileSystem(path=['a'])
        fs.rootdirectory().add(name='Makefile.py',
                               entry=File(lines=["PACKAGE_NAME('xxx')",
                                                 "PACKAGE_VERSION('6.6.6')",
                                                 'IGNORE_ENTRIES(["file"])']))
        fs.rootdirectory().add(name='file',
                               entry=File())
        
        coordinator = BuildCoordinator(
            root=fs.rootdirectory(),
            setups=[])
        filewatcher = FileWatcher(parentbuilder=coordinator.rootbuilder(),
                                  coordinator=coordinator)
        coordinator.rootbuilder().add_builder(filewatcher)
        coordinator.enlarge()

        self.failIf('file' in filewatcher.seen_names())

        pass

    pass

if __name__ == '__main__':
    unittest.main()
    pass
