# Copyright (C) 2006-2007 Joerg Faschingbauer

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

from header.suite_inmem import HeaderInMemorySuite

from libconfix.plugins.c.setups.tests.suite_inmem import SetupsInMemorySuite
from libconfix.plugins.c.relocated_headers.tests.suite_inmem import RelocatedHeadersInMemorySuite
from libconfix.plugins.c.pkg_config.tests.suite_inmem import PkgConfigInMemorySuite

import unittest

class CInMemoryTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(SetupsInMemorySuite())
        self.addTest(RelocatedHeadersInMemorySuite())
        self.addTest(HeaderInMemorySuite())
        self.addTest(PkgConfigInMemorySuite())
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(CInMemoryTestSuite())
    pass
