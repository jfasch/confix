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

from libconfix.core.automake import bootstrap, configure, make, repo_automake
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.hierarchy import DirectorySetupFactory
from libconfix.core.local_package import LocalPackage
from libconfix.core.utils import const
from libconfix.core.utils.error import Error

from libconfix.testutils.persistent import PersistentTestCase

from libconfix.plugins.c.setup import CSetupFactory

import unittest, os, sys, shutil

class InterPackageBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(InterPackageBuildWithLibtool('test'))
        self.addTest(InterPackageBuildWithoutLibtool('test'))
        pass
    pass

class InterPackageBuildBase(PersistentTestCase):
    def __init__(self, str):
        PersistentTestCase.__init__(self, str)
        pass

    def use_libtool(self): assert 0
    
    def setUp(self):
        PersistentTestCase.setUp(self)
        self.sourcedir_ = self.rootpath() + ['source']
        self.builddir_ = self.rootpath() + ['build']
        self.installdir_ = self.rootpath() + ['install']
        self.lo_sourcedir_ = self.sourcedir_ + ['lo']
        self.lo_builddir_ = self.builddir_ + ['lo']
        self.hi_sourcedir_ = self.sourcedir_ + ['hi']
        self.hi_builddir_ = self.builddir_ + ['hi']

        lo_root = Directory()
        lo_root.add(name=const.CONFIX2_IN,
                    entry=File(lines=['PACKAGE_NAME("lo")',
                                      'PACKAGE_VERSION("1.2.3")']))
        lo_root.add(name='lo.h',
                    entry=File(lines=['#ifndef lo_lo_h',
                                      '#define lo_lo_h',
                                      'void lo();',
                                      '#endif',
                                      ]))
        lo_root.add(name='lo.c',
                    entry=File(lines=['#include "lo.h"',
                                      'void lo() {}']))
        self.lo_fs_ = FileSystem(path=self.lo_sourcedir_, rootdirectory=lo_root)

        self.lo_package_ = LocalPackage(rootdirectory=self.lo_fs_.rootdirectory(),
                                        setups=[DirectorySetupFactory(),
                                                CSetupFactory(short_libnames=False,
                                                              use_libtool=self.use_libtool())])
        
        
        hi_root = Directory()
        hi_root.add(name=const.CONFIX2_IN,
                    entry=File(lines=['PACKAGE_NAME("hi")',
                                      'PACKAGE_VERSION("4.5.6")']))
        lib = hi_root.add(name='lib',
                          entry=Directory())
        lib.add(name=const.CONFIX2_IN,
                entry=File())
        lib.add(name='hilib.h',
                entry=File(lines=['#ifndef hi_hilib_h',
                                  '#define hi_hilib_h',
                                  'void hilib();',
                                  '#endif']))
        lib.add(name='hilib.c',
                entry=File(lines=['#include "hilib.h"',
                                  '#include <stdio.h>',
                                  'void hilib() {',
                                  r'    printf("hilib();\n");',
                                  '}']))
        bin = hi_root.add(name='bin',
                          entry=Directory())
        bin.add(name=const.CONFIX2_IN,
                entry=File())
        bin.add(name='main.c',
                entry=File(lines=['#include <lo.h>',
                                  '#include <hilib.h>',
                                  '// URGENCY_ERROR: detect errors as early as possible ',
                                  '// (keeping test-and-fix cycles low)',
                                  '// CONFIX:REQUIRE_H("lo.h", URGENCY_ERROR)',
                                  '// CONFIX:REQUIRE_H("hilib.h", URGENCY_ERROR)',
                                  '',
                                  'int main() {',
                                  '  lo();',
                                  '  hilib();',
                                  '  return 0;',
                                  '}']))

        self.hi_fs_ = FileSystem(path=self.hi_sourcedir_, rootdirectory=hi_root)
        self.hi_package_ = LocalPackage(rootdirectory=self.hi_fs_.rootdirectory(),
                                        setups=[DirectorySetupFactory(),
                                                CSetupFactory(short_libnames=False,
                                                              use_libtool=self.use_libtool())])
        
        pass

    def test(self):
        try:
            # confixize, bootstrap, and install package 'lo'

            self.lo_package_.enlarge(external_nodes=[])
            self.lo_package_.output()
            self.lo_fs_.sync()

            bootstrap.bootstrap(
                packageroot=os.sep.join(self.lo_sourcedir_),
                use_libtool=self.use_libtool(),
                path=None)
            os.makedirs(os.sep.join(self.lo_builddir_))
            configure.configure(
                packageroot=os.sep.join(self.lo_sourcedir_),
                buildroot=os.sep.join(self.lo_builddir_),
                prefix=os.sep.join(self.installdir_))
            make.make(
                dir=os.sep.join(self.lo_builddir_),
                args=['install'])

            # read repo from prefix
            
            automake_repo = repo_automake.AutomakePackageRepository(
                prefix=self.installdir_)
            ext_nodes = []
            for p in automake_repo.packages():
                ext_nodes.extend(p.nodes())
                pass

            # confixize, bootstrap, and install package 'hi'

            self.hi_package_.enlarge(external_nodes=ext_nodes)
            self.hi_package_.output()
            self.hi_fs_.sync()

            bootstrap.bootstrap(
                packageroot=os.sep.join(self.hi_sourcedir_),
                use_libtool=self.use_libtool(),
                path=None)
            os.makedirs(os.sep.join(self.hi_builddir_))
            configure.configure(
                packageroot=os.sep.join(self.hi_sourcedir_),
                buildroot=os.sep.join(self.hi_builddir_),
                prefix=os.sep.join(self.installdir_))
            make.make(
                dir=os.sep.join(self.hi_builddir_),
                args=['install'])
            
        except Error, e:
            sys.stderr.write(`e`+'\n')
            raise

        pass
    pass

class InterPackageBuildWithLibtool(InterPackageBuildBase):
    def __init__(self, str):
        InterPackageBuildBase.__init__(self, str)
        pass
    def use_libtool(self): return True
    pass
    
class InterPackageBuildWithoutLibtool(InterPackageBuildBase):
    def __init__(self, str):
        InterPackageBuildBase.__init__(self, str)
        pass
    def use_libtool(self): return False
    

if __name__ == '__main__':
    unittest.TextTestRunner().run(InterPackageBuildSuite())
    pass
