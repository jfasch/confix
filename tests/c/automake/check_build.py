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

from libconfix.core.local_package import LocalPackage
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.utils import const
from libconfix.core.automake import bootstrap, configure, make
from libconfix.testutils.persistent import PersistentTest

from libconfix.plugins.c.setup import CSetupFactory

import os, unittest

class CheckProgramSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(CheckProgramWithLibtool('test'))
        self.addTest(CheckProgramWithoutLibtool('test'))
        pass
    pass

class CheckProgramBase(unittest.TestCase, PersistentTest):
    def __init__(self, str):
        unittest.TestCase.__init__(self, str)
        PersistentTest.__init__(self)
        pass

    def setUp(self): PersistentTest.setUp(self)
    def tearDown(self): PersistentTest.tearDown(self)
    def use_libtool(self): assert 0

    def test(self):
        fs = FileSystem(path=self.rootpath())

        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())

        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        source.add(
            name=const.CONFIX2_IN,
            entry=File(lines=['PACKAGE_NAME("CheckProgramTest")',
                              'PACKAGE_VERSION("1.2.3")']))
        source.add(
            name='_check_proggy.c',
            entry=File(lines=['extern int open(const char *pathname, int flags);',
                              'int main(void) {',
                              '    return open("'+os.sep.join(build.abspath()+['my-check-was-here'])+'", O_RDWR);',
                              '}']))
        
        package = LocalPackage(root=source,
                               setups=[CSetupFactory(short_libnames=False,
                                                     use_libtool=self.use_libtool())])
        package.enlarge(external_nodes=[])
        package.output()
        fs.sync()

        bootstrap.bootstrap(packageroot=os.sep.join(source.abspath()),
                            path=None,
                            use_libtool=self.use_libtool())
        configure.configure(packageroot=os.sep.join(source.abspath()),
                            buildroot=os.sep.join(build.abspath()),
                            prefix='/dev/null')
        make.make(dir=os.sep.join(build.abspath()),
                  args=['check'])

        self.failUnless(os.path.isfile(os.sep.join(build.abspath()+['my-check-was-here'])))
        pass
    pass

class CheckProgramWithLibtool(CheckProgramBase):
    def use_libtool(self): return True
    pass

class CheckProgramWithoutLibtool(CheckProgramBase):
    def use_libtool(self): return False
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(CheckProgramSuite())
    pass

