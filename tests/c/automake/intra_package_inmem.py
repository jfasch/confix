# $Id: FILE-HEADER,v 1.4 2006/02/06 21:07:44 jfasch Exp $

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

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.local_package import LocalPackage
from libconfix.core.hierarchy import DirectorySetupFactory
from libconfix.core.utils.error import Error
from libconfix.core.automake import bootstrap, configure, make

from libconfix.plugins.c.setup import CSetupFactory
from libconfix.testutils import packages, find

import unittest, os, sys, shutil

class IntraPackageInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(IntraPackageInMemoryTest('test_includepath'))
        pass
    pass

class IntraPackageInMemoryTest(unittest.TestCase):
    def setUp(self):
        self.fs_ = FileSystem(path=['x'],
                              rootdirectory=packages.lo_hi1_hi2_highest_exe(name='self.__class__.__name__',
                                                                            version='1.2.3'))
        
        self.package_ = LocalPackage(root=self.fs_.rootdirectory(),
                                     setups=[DirectorySetupFactory(),
                                             CSetupFactory(short_libnames=False,
                                                           use_libtool=False)])
        self.package_.enlarge(external_nodes=[])
        self.package_.output()
        pass

    def test_includepath(self):
        hi1 = find.find_entrybuilder(root=self.package_.rootbuilder(), path=['hi1'])
        self.failUnless('-I$(top_builddir)/confix_include' in hi1.makefile_am().includepath())
        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(IntraPackageInMemorySuite())
    pass

