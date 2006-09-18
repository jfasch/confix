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

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.utils import const
from libconfix.core.local_package import LocalPackage

from libconfix.plugins.c.setup import CSetup
from libconfix.plugins.c.library import LibraryBuilder

class LibtoolVersionSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(LibtoolVersionTest('test'))
        pass
    pass

class LibtoolVersionTest(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_IN,
            entry=File(lines=["PACKAGE_NAME('LibtoolVersionTest')",
                              "PACKAGE_VERSION('1.2.3')",
                              "LIBTOOL_LIBRARY_VERSION((6,6,6))"]))
        fs.rootdirectory().add(
            name='file.c',
            entry=File())
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[CSetup(short_libnames=False,
                                              use_libtool=True)])
        package.enlarge(external_nodes=[])

        for b in package.rootbuilder().builders():
            if isinstance(b, LibraryBuilder):
                lib_builder = b
                break
            pass
        else:
            self.fail()
            pass

        self.failUnlessEqual(lib_builder.libtool_version_info(), (6,6,6))
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(LibtoolVersionSuite())
    pass
