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

from naked_package import NakedPackageSuite
from dirsetup import BasicDirectorySetupSuite
from filesystests import FileSystemTestSuite
from ignored_entries import IgnoredEntriesSuite
from property import PropertySuite
from iface import BuilderInterfaceTestSuite
from resolve import ResolveTestSuite
from relate import RelateTestSuite
from package_file import PackageFileSuite
from automake.suite import AutomakeSuite
from config.suite import ConfigSuite

import unittest

class BasicTestSuite(unittest.TestSuite):

    def __init__(self):
        unittest.TestSuite.__init__(self)

        self.addTest(NakedPackageSuite())
        self.addTest(FileSystemTestSuite())
        self.addTest(BasicDirectorySetupSuite())
        self.addTest(IgnoredEntriesSuite())
        self.addTest(PropertySuite())
        self.addTest(BuilderInterfaceTestSuite())
        self.addTest(ResolveTestSuite())
        self.addTest(RelateTestSuite())
        self.addTest(PackageFileSuite())
        self.addTest(AutomakeSuite())
        self.addTest(ConfigSuite())
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(BasicTestSuite())
    pass
