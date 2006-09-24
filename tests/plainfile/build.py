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

import os
import sys
import unittest

from libconfix.testutils.persistent import PersistentTestCase
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.directory import Directory
from libconfix.core.local_package import LocalPackage
from libconfix.core.hierarchy.setup import DirectorySetup
from libconfix.core.automake import bootstrap, configure, make

from libconfix.plugins.plainfile.builder import PlainFileBuilder
from libconfix.plugins.plainfile.setup import PlainFileSetup

from package import make_package

class BuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(BuildPlainFileTest('test'))
        pass
    pass

class BuildPlainFileTest(PersistentTestCase):
    def test(self):
        source = make_package()
    
        fs = FileSystem(path=self.rootpath())
        fs.rootdirectory().add(
            name='source',
            entry=source)
        fs.rootdirectory().add(
            name='build',
            entry=Directory())
        fs.rootdirectory().add(
            name='install',
            entry=Directory())

        package = LocalPackage(rootdirectory=source,
                               setups=[DirectorySetup(), PlainFileSetup()])
        package.enlarge(external_nodes=[])
        package.output()
        fs.sync()

        bootstrap.bootstrap(
            packageroot=self.rootpath() + ['source'],
            path=None,
            use_libtool=False, # actually, plain files don't care
            argv0=sys.argv[0])
        configure.configure(
            packageroot=self.rootpath() + ['source'],
            builddir=self.rootpath() + ['build'],
            prefix=self.rootpath() + ['install'])
        make.make(builddir=self.rootpath() + ['build'], args=['install'])
        
        self.failUnless(os.path.isfile(os.sep.join(
            self.rootpath()+['install', 'share', 'subdir', 'data', 'plainfile_data'])))
        self.failUnless(os.path.isfile(os.sep.join(
            self.rootpath()+['install', 'subdir', 'prefix', 'plainfile_prefix'])))

        pass
    pass        

if __name__ == '__main__':
    unittest.TextTestRunner().run(BuildSuite())
    pass

