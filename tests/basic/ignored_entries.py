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
from libconfix.core.local_package import LocalPackage
from libconfix.core.utils import const
from libconfix.testutils import dirhier

import unittest

class FileWatcher(Builder):
    def __init__(self, parentbuilder, package):
        Builder.__init__(
            self,
            id=str(self.__class__)+'('+str(parentbuilder)+')',
            parentbuilder=parentbuilder,
            package=package)
        self.seen_names_ = set()
        pass

    def seen_names(self):
        return self.seen_names_

    def enlarge(self):
        rv = Builder.enlarge(self)
        for name, entry in self.parentbuilder().entries():
            self.seen_names_.add(name)
            pass
        return rv
    pass

class IgnoredEntries(unittest.TestCase):

    def test(self):
        fs = FileSystem(path=['a'])
        fs.rootdirectory().add(name=const.CONFIX2_IN,
                               entry=File(lines=["PACKAGE_NAME('xxx')",
                                                 "PACKAGE_VERSION('6.6.6')",
                                                 'IGNORE_ENTRIES(["file"])']))
        fs.rootdirectory().add(name='file',
                               entry=File())
        
        package = LocalPackage(
            rootdirectory=fs.rootdirectory(),
            setups=[])
        filewatcher = FileWatcher(parentbuilder=package.rootbuilder(),
                                  package=package)
        package.rootbuilder().add_builder(filewatcher)
        package.enlarge(external_nodes=[])

        self.failIf('file' in filewatcher.seen_names())

        pass

    pass

if __name__ == '__main__':
    unittest.main()
    pass
