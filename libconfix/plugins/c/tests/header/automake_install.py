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

from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

from libconfix.plugins.c.setup import DefaultCSetup

from libconfix.testutils import dirhier, makefileparser

class AutomakeInstallInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(BasicHeaderInstallTest('test_zerodeep'))
        self.addTest(BasicHeaderInstallTest('test_onedeep'))
        self.addTest(BasicHeaderInstallTest('test_twodeep'))
        pass
    pass

class BasicHeaderInstallTest(unittest.TestCase):
    def test_zerodeep(self):
        fs = dirhier.packageroot()
        file_h = fs.rootdirectory().add(name='file.h',
                                        entry=File())
        file_h.set_property(name='INSTALLPATH_CINCLUDE', value=[])
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DefaultCSetup(short_libnames=False,
                                              use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        directory_definition = package.rootbuilder().makefile_am().install_directories().get('')
        self.failIf(directory_definition is None)
        self.failUnless(directory_definition.dirname() is None)
        self.failIf(directory_definition.files('HEADERS') is None)
        self.failUnless(directory_definition.files('HEADERS') == ['file.h'])

        # check rules and their dependencies:
        
        # all-local -> confix-install-local -> $(top_builddir)/confix_include/file.h -> $(top_builddir)/confix_include

        confix_install_local = makefileparser.find_rule(
            targets=['confix-install-local'],
            elements=package.rootbuilder().makefile_am().elements())
        install_file_h = makefileparser.find_rule(
            targets=['$(top_builddir)/confix_include/file.h'],
            elements=package.rootbuilder().makefile_am().elements())
        mkdir = makefileparser.find_rule(
            targets=['$(top_builddir)/confix_include'],
            elements=package.rootbuilder().makefile_am().elements())
        self.failIf(confix_install_local is None)
        self.failIf(install_file_h is None)
        self.failIf(mkdir is None)
        self.failUnless('confix-install-local' in package.rootbuilder().makefile_am().all_local().prerequisites())
        self.failUnless('$(top_builddir)/confix_include/file.h' in confix_install_local.prerequisites())

        # clean-local -> confix-clean-local -> $(top_builddir)/confix_include/file.h-clean

        confix_clean_local = makefileparser.find_rule(
            targets=['confix-clean-local'],
            elements=package.rootbuilder().makefile_am().elements())
        clean_file_h = makefileparser.find_rule(
            targets=['$(top_builddir)/confix_include/file.h-clean'],
            elements=package.rootbuilder().makefile_am().elements())
        self.failIf(confix_clean_local is None)
        self.failIf(clean_file_h is None)
        self.failUnless('confix-clean-local' in package.rootbuilder().makefile_am().clean_local().prerequisites())
        self.failUnless('$(top_builddir)/confix_include/file.h-clean' in confix_clean_local.prerequisites())
        
        pass

    def test_onedeep(self):

        fs = dirhier.packageroot()
        file_h = fs.rootdirectory().add(name='file.h',
                                        entry=File())
        file_h.set_property(name='INSTALLPATH_CINCLUDE', value=['xxx'])
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DefaultCSetup(short_libnames=False,
                                              use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        directory_definition = package.rootbuilder().makefile_am().install_directories().get('publicheader_xxx')
        self.failIf(directory_definition is None)
        self.failUnless(directory_definition.dirname() == '$(includedir)/xxx')
        self.failIf(directory_definition.files('HEADERS') is None)
        self.failUnless(directory_definition.files('HEADERS') == ['file.h'])
        pass

    def test_twodeep(self):
        fs = dirhier.packageroot()
        file_h = fs.rootdirectory().add(name='file.h',
                                        entry=File())
        file_h.set_property(name='INSTALLPATH_CINCLUDE', value=['xxx/yyy'])
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DefaultCSetup(short_libnames=False,
                                              use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        directory_definition = package.rootbuilder().makefile_am().install_directories().get('publicheader_xxxyyy')
        self.failIf(directory_definition is None)
        self.failUnless(directory_definition.dirname() == '$(includedir)/xxx/yyy')
        self.failIf(directory_definition.files('HEADERS') is None)
        self.failUnless(directory_definition.files('HEADERS') == ['file.h'])
        pass
        
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(DefaultInstallerSuite())
    pass