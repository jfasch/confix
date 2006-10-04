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
from libconfix.core.utils import const
from libconfix.core.local_package import LocalPackage

from libconfix.testutils import find

from libconfix.plugins.idl.setup import IDLSetup

class BasicIDLSuiteInMemory(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(BasicIDLTest('test'))
        self.addTest(NoInternalRequiresTest('test'))
        pass
    pass

class BasicIDLTest(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=['don\'t', 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('BasicIDLTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())

        fs.rootdirectory().add(
            name='file.idl',
            entry=File(lines=["module A {",
                              "  module B {",
                              "    // ...",
                              "  }; // /module",
                              "}; // /module"]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[IDLSetup()])
        package.boil(external_nodes=[])
        idl_builder = find.find_entrybuilder(rootbuilder=package.rootbuilder(),
                                             path=['file.idl'])
        self.failIf(idl_builder is None)
        self.failUnless(idl_builder.install_path() == ['A', 'B'])
        pass
    pass

class NoInternalRequiresTest(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=['don\'t', 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('BasicIDLTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())

        fs.rootdirectory().add(
            name='file1.idl',
            entry=File(lines=["#include <file2.idl>"]))
        fs.rootdirectory().add(
            name='file2.idl',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[IDLSetup()])
        package.boil(external_nodes=[])
        print str([str(r) for r in package.rootbuilder().requires()])
        self.failIf(len(package.rootbuilder().requires()) != 0)
        pass
    pass
    
if __name__ == '__main__':
    unittest.TextTestRunner().run(BasicIDLSuiteInMemory())
    pass

