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

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.hierarchy.setup import DirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

from libconfix.testutils import find

from libconfix.plugins.c.h import HeaderBuilder
from libconfix.plugins.c.setups.default_setup import DefaultCSetup

class InstallInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(FilePropertyOnly('test'))
        self.addTest(IfaceOnly('test'))
        self.addTest(IfaceFilePropertyConflict('test'))
        self.addTest(Namespace('testSimple'))
        self.addTest(Namespace('testNested'))
        self.addTest(Namespace('testGlobal'))
        self.addTest(Namespace('testAmbiguousFlat'))
        self.addTest(Namespace('testAmbiguousNested'))
        self.addTest(Namespace('testDirectory'))
        self.addTest(InstallPriorities('test'))
        self.addTest(INSTALLDIR_H_EmptyString('test'))
        self.addTest(BadNamespace('test'))
        self.addTest(BadNamespaceGoodINSTALLDIR_H('test'))
        pass
    pass

class FilePropertyOnly(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=[]))
        file.set_property(name='INSTALLPATH_CINCLUDE', value=['xxx'])
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DefaultCSetup(use_libtool=False, short_libnames=False)])
        package.boil(external_nodes=[])

        file_h_builder = find.find_entrybuilder(rootbuilder=package.rootbuilder(), path=['file.h'])
        self.failIf(file_h_builder is None)
        self.failUnless(isinstance(file_h_builder, HeaderBuilder))

        self.failUnlessEqual(file_h_builder.visible_in_directory(), ['xxx'])
        pass
    pass

class IfaceOnly(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=["// CONFIX:INSTALLPATH(['xxx'])"]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DefaultCSetup(use_libtool=False, short_libnames=False)])
        package.boil(external_nodes=[])

        file_h_builder = find.find_entrybuilder(rootbuilder=package.rootbuilder(), path=['file.h'])
        self.failIf(file_h_builder is None)
        self.failUnless(isinstance(file_h_builder, HeaderBuilder))

        self.failUnlessEqual(file_h_builder.visible_in_directory(), ['xxx'])
        pass
    pass

class Namespace(unittest.TestCase):
    def testSimple(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=['namespace A {',
                              '}; // /namespace']))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DefaultCSetup(use_libtool=False, short_libnames=False)])
        package.boil(external_nodes=[])

        file_h_builder = find.find_entrybuilder(rootbuilder=package.rootbuilder(), path=['file.h'])
        self.failIf(file_h_builder is None)
        self.failUnless(isinstance(file_h_builder, HeaderBuilder))
        
        self.failUnlessEqual(file_h_builder.visible_in_directory(), ['A'])
        pass

    def testNested(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=['namespace A {',
                              'namespace B {',
                              '}; // /namespace',
                              '}; // /namespace']))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DefaultCSetup(use_libtool=False, short_libnames=False)])
        package.boil(external_nodes=[])

        file_h_builder = find.find_entrybuilder(rootbuilder=package.rootbuilder(), path=['file.h'])
        self.failIf(file_h_builder is None)
        self.failUnless(isinstance(file_h_builder, HeaderBuilder))

        self.failUnlessEqual(file_h_builder.visible_in_directory(), ['A', 'B'])
        pass

    def testGlobal(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=[]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DefaultCSetup(use_libtool=False, short_libnames=False)])
        package.boil(external_nodes=[])

        file_h_builder = find.find_entrybuilder(rootbuilder=package.rootbuilder(), path=['file.h'])
        self.failIf(file_h_builder is None)
        self.failUnless(isinstance(file_h_builder, HeaderBuilder))

        self.failUnlessEqual(file_h_builder.visible_in_directory(), [])
        pass

    def testAmbiguousFlat(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=['namespace A {',
                              '}; // /namespace',
                              'namespace B {',
                              '}; // /namespace'
                              ]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DefaultCSetup(use_libtool=False, short_libnames=False)])
        try:
            package.boil(external_nodes=[])
        except HeaderBuilder.BadNamespace:
            return
        self.fail()
        pass
    def testAmbiguousNested(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=['namespace A {',
                              ' namespace A1 {',
                              ' }; // /namespace',
                              '}; // /namespace',
                              'namespace A {',
                              ' namespace A2 {',
                              ' }; // /namespace',
                              '}; // /namespace'
                              ]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DefaultCSetup(use_libtool=False, short_libnames=False)])
        try:
            package.boil(external_nodes=[])
        except HeaderBuilder.BadNamespace:
            return
        self.fail()
        pass
    def testDirectory(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(name=const.CONFIX2_PKG,
                               entry=File(lines=["PACKAGE_NAME('xxx')",
                                                 "PACKAGE_VERSION('6.6.6')"]))
        fs.rootdirectory().add(name=const.CONFIX2_DIR,
                               entry=File(lines=["SET_FILE_PROPERTY(",
                                                 "    filename='file.h', ",
                                                 "    name='INSTALLPATH_CINCLUDE',",
                                                 "    value=['xxx'])"]))
        fs.rootdirectory().add(name='file.h', entry=File(lines=[]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DefaultCSetup(short_libnames=False,
                                              use_libtool=False)])
        package.boil(external_nodes=[])

        file_h_builder = find.find_entrybuilder(rootbuilder=package.rootbuilder(), path=['file.h'])
        self.failIf(file_h_builder is None)
        self.failUnless(isinstance(file_h_builder, HeaderBuilder))

        self.failUnlessEqual(file_h_builder.visible_in_directory(), ['xxx'])
        pass
    pass

class IfaceFilePropertyConflict(unittest.TestCase):
    def runTest(self): self.test()
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=["// CONFIX:INSTALLPATH(['xxx'])"]))
        file.set_property(name='INSTALLPATH_CINCLUDE', value=['xxx'])
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DefaultCSetup(short_libnames=False,
                                              use_libtool=False)])
        try:
            package.boil(external_nodes=[])
        except HeaderBuilder.AmbiguousVisibility, e:
            return
        self.fail()
        pass
    pass

class InstallPriorities(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=['don\'t', 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('HeaderInstallInterfaceTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["INSTALLDIR_H('install/from/dir/iface')"]))
        fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=['namespace install {',
                              'namespace from {',
                              'namespace ns {',
                              'namespace hierarchy {',
                              '} // /namespace',
                              '} // /namespace',
                              '} // /namespace',
                              '} // /namespace',
                              ]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DefaultCSetup(use_libtool=False, short_libnames=False)])
        package.boil(external_nodes=[])

        file_h_builder = find.find_entrybuilder(rootbuilder=package.rootbuilder(), path=['file.h'])
        self.failIf(file_h_builder is None)
        self.failUnless(isinstance(file_h_builder, HeaderBuilder))

        self.failUnlessEqual(file_h_builder.visible_in_directory(), ['install','from','dir','iface'])
        pass
    pass

class INSTALLDIR_H_EmptyString(unittest.TestCase):

    # this comes out of a regression I had one day. INSTALLDIR_H('')
    # led to headerfiles being provided as '/file.h' rather than
    # 'file.h'.
    
    def test(self):
        fs = FileSystem(path=['don\'t', 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('HeaderInstallInterfaceTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())

        lo = fs.rootdirectory().add(
            name='lo',
            entry=Directory())
        lo.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["INSTALLDIR_H('')"]))
        lo.add(
            name='lo.h',
            entry=File())
        
        hi = fs.rootdirectory().add(
            name='hi',
            entry=Directory())
        hi.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=[]))
        hi.add(
            name='hi.cc',
            entry=File(lines=["//CONFIX:REQUIRE_H('lo.h', REQUIRED)"]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DirectorySetup(),
                                       DefaultCSetup(use_libtool=False, short_libnames=False)])
        package.boil(external_nodes=[])
        pass
    pass

class BadNamespace(unittest.TestCase):
    """
    A bad namespace, and no idea where to install file.h
    """
    def test(self):
        rootdirectory = Directory()
        rootdirectory.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        rootdirectory.add(
            name=const.CONFIX2_DIR,
            entry=File())
        rootdirectory.add(
            name='file.h',
            entry=File(lines=['namespace X {',
                              '}']))

        package = LocalPackage(rootdirectory=rootdirectory,
                               setups=[DefaultCSetup(use_libtool=False, short_libnames=False)])
        try:
            package.boil(external_nodes=[])
        except HeaderBuilder.BadNamespace:
            pass
        pass
    pass

class BadNamespaceGoodINSTALLDIR_H(unittest.TestCase):
    """
    Explicit INSTALLDIR_H() covers bad namespace.
    """
    def test(self):
        rootdirectory = Directory()
        rootdirectory.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        rootdirectory.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['INSTALLDIR_H("")']))
        rootdirectory.add(
            name='file.h',
            entry=File(lines=['namespace X {',
                              '}']))

        package = LocalPackage(rootdirectory=rootdirectory,
                               setups=[DefaultCSetup(use_libtool=False, short_libnames=False)])
        package.boil(external_nodes=[])
        pass
    pass
        

if __name__ == '__main__':
    unittest.TextTestRunner().run(InstallInMemorySuite())
    pass

