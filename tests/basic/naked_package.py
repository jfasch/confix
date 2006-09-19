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

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.utils import const
from libconfix.core.local_package import LocalPackage

class NakedPackageSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(NakedPackageTest('test'))
        pass
    pass

class NakedPackageTest(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=['','path','to','package'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("TheNakedPackage")',
                              'PACKAGE_VERSION("1.2.3")']))
        # add Confix2.dir for no real reason. we could really do
        # without, and should take some time to investigate. but not
        # now (now==2006-09-19).
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File([]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[])
        self.failUnlessEqual(package.name(), 'TheNakedPackage')
        self.failUnlessEqual(package.version(), '1.2.3')
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(NakedPackageSuite())
    pass
