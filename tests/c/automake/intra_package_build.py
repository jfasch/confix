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
from libconfix.core.coordinator import BuildCoordinator
from libconfix.core.hierarchy import DirectorySetupFactory
from libconfix.core.utils.error import Error
from libconfix.core.automake import bootstrap, configure, make

from libconfix.plugins.c.setup import CSetupFactory
from libconfix.testutils import packages

import unittest, os, sys, shutil

class IntraPackageBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(IntraPackageBuildTest('test'))
        pass
    pass

class IntraPackageBuildTest(unittest.TestCase):
    def __init__(self, str):
        unittest.TestCase.__init__(self, str)
        self.seqnum_ = 0
        pass

    def setUp(self):
        self.rootpath_ = ['', 'tmp', 'confix.'+self.__class__.__name__+'.'+str(self.seqnum_)+'.'+str(os.getpid())]
        self.seqnum_ += 1
        self.sourcerootpath_ = self.rootpath_ + ['source']
        self.buildrootpath_ = self.rootpath_ + ['build']

        self.fs_ = FileSystem(path=self.sourcerootpath_,
                              rootdirectory=packages.lo_hi1_hi2_highest_exe(name='intrapackagebuildtest',
                                                                            version='1.2.3'))
        
        self.coordinator_ = BuildCoordinator(root=self.fs_.rootdirectory(),
                                             setups=[DirectorySetupFactory(),
                                                     CSetupFactory(short_libnames=False,
                                                                   use_libtool=False)])
        self.coordinator_.enlarge()
        self.coordinator_.output()
        self.fs_.sync()
        pass

    def tearDown(self):
##         dir = os.sep.join(self.rootpath_)
##         if os.path.isdir(dir):
##             shutil.rmtree(dir)
##             pass
        pass

    def test(self):
        try:
            packageroot = os.sep.join(self.sourcerootpath_)
            buildroot = os.sep.join(self.buildrootpath_)
            print packageroot
            print buildroot
            bootstrap.bootstrap(packageroot=packageroot, aclocal_includedirs=[])
            os.makedirs(buildroot)
            configure.configure(packageroot=packageroot, buildroot=buildroot, prefix='/dev/null')
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

if __name__ == '__main__':
    unittest.TextTestRunner().run(IntraPackageBuildSuite())
    pass

