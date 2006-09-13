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

from libconfix.testutils import packages
from libconfix.testutils.persistent import PersistentTestCase

from libconfix.plugins.c.setup import CSetupFactory

import unittest, os, sys, shutil

class IntraPackageBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(IntraPackageBuildWithLibtool('test'))
        self.addTest(IntraPackageBuildWithoutLibtool('test'))
        pass
    pass

class IntraPackageBuildBase(PersistentTestCase):
    def __init__(self, methodName):
        PersistentTestCase.__init__(self, methodName)
        pass

    def use_libtool(self): assert 0

    def setUp(self):
        PersistentTestCase.setUp(self)
        
        self.sourcerootpath_ = self.rootpath() + ['source']
        self.buildrootpath_ = self.rootpath() + ['build']

        self.fs_ = FileSystem(path=self.sourcerootpath_,
                              rootdirectory=packages.lo_hi1_hi2_highest_exe(name='intrapackagebuildtest',
                                                                            version='1.2.3'))
        
        self.package_ = LocalPackage(rootdirectory=self.fs_.rootdirectory(),
                                     setups=[DirectorySetupFactory(),
                                             CSetupFactory(short_libnames=False,
                                                           use_libtool=self.use_libtool())])
        self.package_.enlarge(external_nodes=[])
        self.package_.output()
        self.fs_.sync()
        pass

    def test(self):
        try:
            packageroot = os.sep.join(self.sourcerootpath_)
            buildroot = os.sep.join(self.buildrootpath_)
            bootstrap.bootstrap(
                packageroot=packageroot,
                path=None,
                use_libtool=self.use_libtool())
            os.makedirs(buildroot)
            configure.configure(
                packageroot=packageroot,
                buildroot=buildroot,
                prefix='/dev/null')
            make.make(dir=buildroot, args=[])
        except Error, e:
            sys.stderr.write(`e`+'\n')
            raise
        
        self.failUnless(os.path.isfile(os.sep.join(self.buildrootpath_+['lo', 'lo.o'])))
        self.failUnless(os.path.isfile(os.sep.join(self.buildrootpath_+['hi1', 'hi1.o'])))
        self.failUnless(os.path.isfile(os.sep.join(self.buildrootpath_+['hi2', 'hi2.o'])))
        self.failUnless(os.path.isfile(os.sep.join(self.buildrootpath_+['highest', 'highest.o'])))
        self.failUnless(os.path.isfile(os.sep.join(self.buildrootpath_+['exe', 'main.o'])))
        self.failUnless(os.path.isfile(os.sep.join(self.buildrootpath_+['exe', 'intrapackagebuildtest_exe_main'])))
        pass

    pass

class IntraPackageBuildWithLibtool(IntraPackageBuildBase):
    def __init__(self, str):
        IntraPackageBuildBase.__init__(self, str)
        pass
    def use_libtool(self): return True
    pass

class IntraPackageBuildWithoutLibtool(IntraPackageBuildBase):
    def __init__(self, str):
        IntraPackageBuildBase.__init__(self, str)
        pass
    def use_libtool(self): return False
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(IntraPackageBuildSuite())
    pass

