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

from libconfix.core.utils import const
from libconfix.core.utils.error import Error
from libconfix.core.automake import bootstrap, configure, make
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.local_package import LocalPackage
from libconfix.core.hierarchy import DirectorySetupFactory

from libconfix.plugins.c.setup import CSetupFactory

import unittest, os, sys, shutil

class SimpleBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(SimpleBuildTest('test'))
        pass
    pass

class SimpleBuildTest(unittest.TestCase):
    def __init__(self, str):
        unittest.TestCase.__init__(self, str)
        self.seqnum_ = 0
        pass
    def setUp(self):
        try:
            self.rootpath_ = ['', 'tmp', 'confix.'+self.__class__.__name__+'.'+str(self.seqnum_)+'.'+str(os.getpid())]
            self.sourcerootpath_ = self.rootpath_ + ['source']
            self.fs_ = FileSystem(path=self.sourcerootpath_)

            self.buildrootpath_ = self.rootpath_ + ['build']
            self.seqnum_ += 1

            self.fs_.rootdirectory().add('Makefile.py',
                                         File(lines=['PACKAGE_NAME("simplebuildtest")',
                                                     'PACKAGE_VERSION("6.6.6")']))
            self.fs_.rootdirectory().add(name='file.h',
                                         entry=File(lines=['#ifndef FILE_H',
                                                           '#define FILE_H',
                                                           'extern int i;',
                                                           '#endif',
                                                           ]))
            self.fs_.rootdirectory().add(name='file.c',
                                         entry=File(lines=['#include "file.h"',
                                                           'int i;',
                                                           ]))
            
            self.package_ = LocalPackage(root=self.fs_.rootdirectory(),
                                         setups=[CSetupFactory(short_libnames=False, use_libtool=False)])
            self.package_.enlarge(external_nodes=[])
            self.package_.output()
            self.fs_.sync()
        except Error, e:
            sys.stderr.write(`e`+'\n')
            raise
        pass

    def tearDown(self):
        dir = os.sep.join(self.rootpath_)
        if os.path.isdir(dir):
            shutil.rmtree(dir)
            pass
        pass
        
    def test(self):
        try:
            packageroot = os.sep.join(self.sourcerootpath_)
            buildroot = os.sep.join(self.buildrootpath_)
            bootstrap.bootstrap(packageroot=packageroot, aclocal_includedirs=[])
            os.makedirs(buildroot)
            configure.configure(packageroot=packageroot, buildroot=buildroot, prefix='/dev/null')
            make.make(dir=buildroot, args=[])
        except Error, e:
            sys.stderr.write(`e`+'\n')
            raise

        self.failUnless(os.path.isfile(os.sep.join(self.buildrootpath_+['file.o'])))
        pass

    pass
    
if __name__ == '__main__':
    unittest.TextTestRunner().run(SimpleBuildSuite())
    pass
