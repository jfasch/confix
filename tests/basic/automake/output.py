# $Id: output.py,v 1.1 2006/07/12 08:42:22 jfasch Exp $

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

from libconfix.testutils import dirhier, find
from libconfix.core.utils import const
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.coordinator import BuildCoordinator
from libconfix.core.hierarchy import DirectorySetupFactory
from libconfix.plugins.c.setup import CSetupFactory
from libconfix.plugins.c.library import LibraryBuilder
from libconfix.plugins.c.executable import ExecutableBuilder

import unittest

class AutomakeOutputSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(AutomakeOutputTest('test_subdirs'))
        self.addTest(AutomakeOutputTest('test_configure_ac'))
        self.addTest(AutomakeOutputTest('test_auxdir'))
        self.addTest(AutomakeOutputTest('test_toplevel_makefile_am'))
        self.addTest(AutomakeOutputTest('test_subdir1_makefile_am'))
        self.addTest(AutomakeOutputTest('test_subdir2_makefile_am'))
        self.addTest(AutomakeOutputTest('test_subdir3_makefile_am'))
        pass
    pass

class AutomakeOutputTest(unittest.TestCase):
    def setUp(self):
        self.fs_ = dirhier.packageroot()
        subdir1 = self.fs_.rootdirectory().add(name='subdir1', entry=Directory())
        subdir1.add(name=const.MAKEFILE_PY,
                    entry=File(lines=['PROVIDE_SYMBOL("subdir1")']))
        
        subdir2 = self.fs_.rootdirectory().add(name='subdir2', entry=Directory())
        subdir2.add(name=const.MAKEFILE_PY,
                    entry=File(lines=['PROVIDE_SYMBOL("subdir2")',
                                      'REQUIRE_SYMBOL("subdir1")']))
        subdir3 = self.fs_.rootdirectory().add(name='subdir3', entry=Directory())
        subdir3.add(name=const.MAKEFILE_PY,
                    entry=File(lines=['REQUIRE_SYMBOL("subdir2")']))
        
        self.coordinator_ = BuildCoordinator(root=self.fs_.rootdirectory(),
                                             setups=[DirectorySetupFactory()])
        self.coordinator_.enlarge()
        self.coordinator_.output()

        self.subdir1_builder_ = find.find_entrybuilder(self.coordinator_.rootbuilder(), ['subdir1'])
        self.subdir2_builder_ = find.find_entrybuilder(self.coordinator_.rootbuilder(), ['subdir2'])
        self.subdir3_builder_ = find.find_entrybuilder(self.coordinator_.rootbuilder(), ['subdir3'])
        assert self.subdir1_builder_
        assert self.subdir2_builder_
        assert self.subdir3_builder_

        pass

    def tearDown(self):
        self.fs_ = None
        self.coordinator_ = None
        pass

    def test_subdirs(self):
        self.failIfEqual(self.fs_.rootdirectory().find(['Makefile.am']), None)
        self.failUnless(const.MAKEFILE_PY in self.coordinator_.rootbuilder().makefile_am().extra_dist())

        # relative positions of subdir1, subdir2, subdir3 in SUBDIRS
        # must be subdir1 < subdir2 < subdir3. (we cannot count on
        # absolute positions because the topological range of '.' is
        # random - '.' has no dependencies. (same hold for aux.))

        aux = dot = subdir1 = subdir2 = subdir3 = None

        for i in range(len(self.coordinator_.rootbuilder().makefile_am().subdirs())):
            if self.coordinator_.rootbuilder().makefile_am().subdirs()[i].dirname() == 'confix-admin':
                self.failUnless(aux is None)
                aux = i
            elif self.coordinator_.rootbuilder().makefile_am().subdirs()[i].dirname() == 'subdir1':
                self.failUnless(subdir1 is None)
                subdir1 = i
            elif self.coordinator_.rootbuilder().makefile_am().subdirs()[i].dirname() == 'subdir2':
                self.failUnless(subdir2 is None)
                subdir2 = i
            elif self.coordinator_.rootbuilder().makefile_am().subdirs()[i].dirname() == 'subdir3':
                self.failUnless(subdir3 is None)
                subdir3 = i
                pass
            elif self.coordinator_.rootbuilder().makefile_am().subdirs()[i].dirname() == '.':
                self.failUnless(dot is None)
                dot = i
                pass
            pass

        # see if there is anything in there at all
        self.failIfEqual(len(self.fs_.rootdirectory().find(['Makefile.am']).lines()), 0)

        self.failIf(aux is None)
        self.failIf(dot is None)
        self.failIf(subdir1 is None)
        self.failIf(subdir2 is None)
        self.failIf(subdir3 is None)

        self.failUnless(subdir1 < subdir2 < subdir3)
        
        pass

    def test_configure_ac(self):
        self.failIfEqual(self.fs_.rootdirectory().find(['configure.ac']), None)
        self.failUnless('config.h' in self.coordinator_.configure_ac().ac_config_headers())
        self.failIf(self.coordinator_.configure_ac().packagename() is None)
        self.failIf(self.coordinator_.configure_ac().packageversion() is None)
        pass

    def test_auxdir(self):
        auxdir = self.coordinator_.rootbuilder().directory().find(['confix-admin'])
        self.failIf(auxdir is None)
        mf_am = auxdir.find(['Makefile.am'])
        self.failIf(mf_am is None)
        self.failUnlessEqual(self.coordinator_.configure_ac().ac_config_aux_dir(), 'confix-admin')
        config_ac = self.fs_.rootdirectory().find(['configure.ac'])
        self.failIf(config_ac is None)
        for line in config_ac.lines():
            if line.find('AC_CONFIG_AUX_DIR') != -1 and line.find('confix-admin') != -1:
                break
            pass
        else:
            self.fail()
            pass        
        pass

    def test_toplevel_makefile_am(self):
        mf_am = self.coordinator_.rootbuilder().makefile_am()
        self.failUnless('1.9' in mf_am.automake_options())
        self.failUnless('dist-bzip2' in mf_am.automake_options())
        self.failUnless('dist-shar' in mf_am.automake_options())
        self.failUnless('dist-zip' in mf_am.automake_options())
        self.failUnless(const.MAKEFILE_PY in mf_am.extra_dist())
        self.failUnless(self.coordinator_.name()+'.repo' in mf_am.extra_dist())
        self.failUnless('Makefile.in' in mf_am.maintainercleanfiles())
        self.failUnless('Makefile.am' in mf_am.maintainercleanfiles())
        pass

    def test_subdir1_makefile_am(self):
        self.failIfEqual(self.fs_.rootdirectory().find(['subdir1', 'Makefile.am']), None)
        self.failUnless(const.MAKEFILE_PY in self.subdir1_builder_.makefile_am().extra_dist())
        self.failUnless('Makefile.in' in self.subdir1_builder_.makefile_am().maintainercleanfiles())
        self.failUnless('Makefile.am' in self.subdir1_builder_.makefile_am().maintainercleanfiles())
        pass

    def test_subdir2_makefile_am(self):
        self.failIfEqual(self.fs_.rootdirectory().find(['subdir2', 'Makefile.am']), None)
        self.failUnless(const.MAKEFILE_PY in self.subdir2_builder_.makefile_am().extra_dist())
        self.failUnless('Makefile.in' in self.subdir2_builder_.makefile_am().maintainercleanfiles())
        self.failUnless('Makefile.am' in self.subdir2_builder_.makefile_am().maintainercleanfiles())
        pass

    def test_subdir3_makefile_am(self):
        self.failIfEqual(self.fs_.rootdirectory().find(['subdir3', 'Makefile.am']), None)
        self.failUnless(const.MAKEFILE_PY in self.subdir3_builder_.makefile_am().extra_dist())
        self.failUnless('Makefile.in' in self.subdir3_builder_.makefile_am().maintainercleanfiles())
        self.failUnless('Makefile.am' in self.subdir3_builder_.makefile_am().maintainercleanfiles())
        pass

    pass

if __name__ == '__main__':
    unittest.main()
    pass
    
