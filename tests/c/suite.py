# $Id: suite.py,v 1.9 2006/07/07 15:29:18 jfasch Exp $

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

from setup_library import LibrarySetupSuite
from setup_exe import ExecutableSetupTest
from main_search import MainSearch
from requires import RequireTestSuite
from install_path import InstallPathSuite
from relate import RelateSuite
from automake.suite import AutomakeCSuite

import unittest

class CTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)

        self.addTest(LibrarySetupSuite())
        self.addTest(ExecutableSetupTest('test'))
        self.addTest(MainSearch('test'))
        self.addTest(RequireTestSuite())
        self.addTest(InstallPathSuite())
        self.addTest(RelateSuite())
        self.addTest(AutomakeCSuite())
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(CTestSuite())
    pass
