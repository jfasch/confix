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

from libconfix.core.filebuilder import FileBuilder
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.hierarchy import DirectorySetupFactory
from libconfix.core.local_package import LocalPackage
from libconfix.core.utils import const

from libconfix.plugins.c.setup import CSetupFactory
from libconfix.plugins.c.h import HeaderBuilder
from libconfix.plugins.c.c import CBuilder
from libconfix.plugins.c.library import LibraryBuilder
from libconfix.testutils import dirhier, find

import unittest

class LibrarySetupSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(LibrarySetupBasic('test'))
        self.addTest(LibraryNames('testLongName'))
        pass
    pass        

class LibrarySetupBasic(unittest.TestCase):
    def test(self):
        fs = dirhier.packageroot()
        fs.rootdirectory().add(name='file.h', entry=File(lines=[]))
        fs.rootdirectory().add(name='file.c', entry=File(lines=[]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[CSetupFactory(short_libnames=False, use_libtool=False)])
        package.enlarge(external_nodes=[])

        file_h_builder = None
        file_c_builder = None
        library_builder = None
        for b in package.rootbuilder().builders():
            if isinstance(b, FileBuilder):
                if b.file().name() == 'file.h' and isinstance(b, HeaderBuilder):
                    file_h_builder = b
                    pass
                if b.file().name() == 'file.c' and isinstance(b, CBuilder):
                    file_c_builder = b
                    pass
                pass
            if isinstance(b, LibraryBuilder):
                library_builder = b
                pass
            pass
        self.failUnless(isinstance(file_h_builder, HeaderBuilder))
        self.failUnless(isinstance(file_c_builder, CBuilder)) 
        self.failUnless(isinstance(library_builder, LibraryBuilder)) 

        self.failUnless(file_h_builder in library_builder.members())
        self.failUnless(file_c_builder in library_builder.members())
        pass
    pass

class LibraryNames(unittest.TestCase):
    def setUp(self):
        self.fs_ = dirhier.packageroot()
        dir1 = self.fs_.rootdirectory().add(name='dir1', entry=Directory())
        dir1.add(name=const.CONFIX2_IN, entry=File(lines=[]))
        dir2 = dir1.add(name='dir2', entry=Directory())
        dir2.add(name=const.CONFIX2_IN, entry=File(lines=[]))
        dir3 = dir2.add(name='dir3', entry=Directory())
        dir3.add(name=const.CONFIX2_IN, entry=File(lines=[]))
        dir3.add(name='file.c', entry=File(lines=[]))
        self.dir3_ = dir3
        pass

    def testLongName(self):
        
        package = LocalPackage(rootdirectory=self.fs_.rootdirectory(),
                               setups=[DirectorySetupFactory(),
                                       CSetupFactory(short_libnames=False,
                                                     use_libtool=False)])
        package.enlarge(external_nodes=[])

        dir3lib_builder = None
        for b in find.find_entrybuilder(package.rootbuilder(), ['dir1', 'dir2', 'dir3']).builders():
            if isinstance(b, LibraryBuilder):
                self.failIf(dir3lib_builder is not None)
                dir3lib_builder = b
                pass
            pass

        self.failUnlessEqual(dir3lib_builder.basename(),
                             '_'.join([package.name()]+self.dir3_.relpath(self.fs_.rootdirectory())))
        pass
    
    def testShortName(self):
        
        package = LocalPackage(rootdirectory=self.fs_.rootdirectory(),
                               setups=[DirectorySetupFactory(),
                                       CSetupFactory(short_libnames=True,
                                                     use_libtool=False)])
        package.enlarge(external_nodes=[])

        dir3lib_builder = None
        for b in find.find_entrybuilder(package.rootbuilder(), ['dir1', 'dir2', 'dir3']).builders():
            if isinstance(b, LibraryBuilder):
                self.failIf(dir3lib_builder is not None)
                dir3lib_builder = b
                pass
            pass

        self.failUnlessEqual(dir3lib_builder.basename(),
                             '_'.join([package.name(), self.dir3_.name()]))
        pass
    pass
    
if __name__ == '__main__':
    unittest.main()
