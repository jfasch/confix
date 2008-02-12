# Copyright (C) 2008 Joerg Faschingbauer

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

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const
from libconfix.testutils.persistent import PersistentTestCase
from libconfix.setups.explicit_setup import ExplicitSetup

import unittest

class CommonDirectoryInterfaceSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)

        self.addTest(CURRENT_BUILDER_Test('test'))
        self.addTest(CURRENT_DIRECTORY_Test('test'))
        self.addTest(ADD_DIRECTORY_Test('test'))
        self.addTest(FIND_ENTRY_Test('test'))
        self.addTest(GET_ENTRIES_Test('test'))
        self.addTest(RESCAN_CURRENT_DIRECTORY_Test('test'))
        pass
    pass

class CURRENT_BUILDER_Test(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["from libconfix.core.filesys.file import File",
                              "if '"+str(fs.rootdirectory())+"' == str(CURRENT_BUILDER().directory()):",
                              "  CURRENT_DIRECTORY().add(name='ok', entry=File())"]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        self.failUnless(package.rootdirectory().get('ok'))
        pass
    pass
        
class CURRENT_DIRECTORY_Test(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["from libconfix.core.filesys.file import File",
                              "if '"+str(fs.rootdirectory())+"' == str(CURRENT_DIRECTORY()):",
                              "  CURRENT_DIRECTORY().add(name='ok', entry=File())"]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        self.failUnless(package.rootdirectory().get('ok'))
        pass
    pass
        
class ADD_DIRECTORY_Test(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["ADD_DIRECTORY('dir')"]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        self.failIf(package.rootdirectory().get('dir') is None)
        self.failUnless(type(package.rootdirectory().get('dir')) is Directory)
        pass
    pass
        
class FIND_ENTRY_Test(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["from libconfix.core.filesys.file import File",
                              "entry = FIND_ENTRY('file')",
                              "if entry is not None and type(entry) is File:",
                              "    CURRENT_DIRECTORY().add(name='ok', entry=File())",
                              ]))
        fs.rootdirectory().add(
            name='file',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        self.failUnless(package.rootdirectory().get('ok'))
        pass
    pass
        
class GET_ENTRIES_Test(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["from libconfix.core.filesys.file import File",
                              "for e in GET_ENTRIES():",
                              "    if e[0] == 'file' and type(e[1]) is File:",
                              "        CURRENT_DIRECTORY().add(name='ok', entry=File())",
                              "        break",
                              ]))
        fs.rootdirectory().add(
            name='file',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        self.failUnless(package.rootdirectory().get('ok'))
        pass
    pass

class RESCAN_CURRENT_DIRECTORY_Test(PersistentTestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))

        self.fail()

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        self.failUnless(package.rootdirectory().get('ok'))
        pass
    pass
        
if __name__ == '__main__':
    unittest.TextTestRunner().run(CommonDirectoryInterfaceSuite())
    pass
