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

from libconfix.plugins.c.h import HeaderBuilder
import libconfix.plugins.c.namespace
from libconfix.plugins.c.setup import CSetupFactory

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.local_package import LocalPackage
from libconfix.core.utils import const

from libconfix.testutils import find

import unittest

class InstallPathSuite(unittest.TestSuite):
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
        pass
    pass

class FilePropertyOnly(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_IN,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        file = fs.rootdirectory().add(
            name='some_file',
            entry=File(lines=[]))
        file.set_property(name='INSTALLPATH_CINCLUDE', value=['xxx'])
        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[])
        builder = HeaderBuilder(file=file, parentbuilder=None, package=package)
        self.failUnlessEqual(builder.install_path(), ['xxx'])
        pass
    pass

class IfaceOnly(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_IN,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        file = fs.rootdirectory().add(
            name='some_file',
            entry=File(lines=["// CONFIX:INSTALLPATH(['xxx'])"]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[])
        builder = HeaderBuilder(file=file, parentbuilder=None, package=package)
        self.failUnlessEqual(builder.install_path(), ['xxx'])
        pass
    pass

class Namespace(unittest.TestCase):
    def testSimple(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_IN,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        file = fs.rootdirectory().add(
            name='some_file',
            entry=File(lines=['namespace A {',
                              '}; // /namespace']))
        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[])
        builder = HeaderBuilder(file=file, parentbuilder=None,  package=package)
        self.failUnlessEqual(builder.install_path(), ['A'])
        pass
    def testNested(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_IN,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        file = fs.rootdirectory().add(
            name='some_file',
            entry=File(lines=['namespace A {',
                              'namespace B {',
                              '}; // /namespace',
                              '}; // /namespace']))
        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[])
        builder = HeaderBuilder(file=file, parentbuilder=None,  package=package)
        self.failUnlessEqual(builder.install_path(), ['A', 'B'])
        pass
    def testGlobal(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_IN,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        file = fs.rootdirectory().add(
            name='some_file',
            entry=File(lines=[]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[])
        builder = HeaderBuilder(file=file, parentbuilder=None,  package=package)
        self.failUnlessEqual(builder.install_path(), [])
        pass
    def testAmbiguousFlat(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_IN,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        file = fs.rootdirectory().add(
            name='file',
            entry=File(lines=['namespace A {',
                              '}; // /namespace',
                              'namespace B {',
                              '}; // /namespace'
                              ]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[])
        try:
            HeaderBuilder(file=file, parentbuilder=None,  package=package)
        except libconfix.plugins.c.namespace.AmbiguousNamespace:
            return
        self.fail()
        pass
    def testAmbiguousNested(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_IN,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        file = fs.rootdirectory().add(
            name='file',
            entry=File(lines=['namespace A {',
                              ' namespace A1 {',
                              ' }; // /namespace',
                              '}; // /namespace',
                              'namespace A {',
                              ' namespace A2 {',
                              ' }; // /namespace',
                              '}; // /namespace'
                              ]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[])
        try:
            HeaderBuilder(file=file, parentbuilder=None,  package=package)
        except libconfix.plugins.c.namespace.AmbiguousNamespace:
            return
        self.fail()
        pass
    def testDirectory(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(name=const.CONFIX2_IN,
                               entry=File(lines=["PACKAGE_NAME('xxx')",
                                                 "PACKAGE_VERSION('6.6.6')",
                                                 "FILE_PROPERTY(",
                                                 "    filename='file.h', ",
                                                 "    name='INSTALLPATH_CINCLUDE',",
                                                 "    value=['xxx'])"]))
        fs.rootdirectory().add(name='file.h', entry=File(lines=[]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[CSetupFactory(short_libnames=False,
                                                     use_libtool=False)])
        package.enlarge(external_nodes=[])
        filebuilder = find.find_entrybuilder(package.rootbuilder(), ['file.h'])
        assert filebuilder is not None
        self.failUnlessEqual(filebuilder.install_path(), ['xxx'])
        pass
    pass

class IfaceFilePropertyConflict(unittest.TestCase):
    def runTest(self): self.test()
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_IN,
            entry=File(['PACKAGE_NAME("argh")',
                        'PACKAGE_VERSION("1.2.3")']))
        file = fs.rootdirectory().add(
            name='file',
            entry=File(lines=["// CONFIX:INSTALLPATH(['xxx'])"]))
        file.set_property(name='INSTALLPATH_CINCLUDE', value=['xxx'])
        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[])
        try:
            builder = HeaderBuilder(file=file, parentbuilder=None, package=package)
        except HeaderBuilder.InstallPathConflict, e:
            return
        self.fail()
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(InstallPathSuite())
    pass

