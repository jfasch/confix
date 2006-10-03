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

import unittest

from libconfix.plugins.c.setup import CSetup

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.utils import const
from libconfix.core.local_package import LocalPackage
from libconfix.testutils import find

class MiscellaneousSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(IgnoredEntriesTest('test'))
        pass
    pass

class IgnoredEntriesTest(unittest.TestCase):

    # a regression I had one day. turned out that IGNORE_FILE() passed
    # a string to DirectoryBuilder's add_ignored_entries() which
    # expects a list.
    
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('IgnoredEntriesTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["IGNORE_FILE('x.cc')"]))
        fs.rootdirectory().add(
            name='x.cc',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[CSetup(use_libtool=False, short_libnames=False)])
        package.boil(external_nodes=[])

        self.failIf(find.find_entrybuilder(rootbuilder=package.rootbuilder(), path=['x.cc']) is not None)
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(MiscellaneousSuite())
    pass

