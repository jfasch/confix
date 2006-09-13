# $Id: suite.py,v 1.1 2006/07/12 08:42:22 jfasch Exp $

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

from makefile_utils import MakefileUtilsSuite
from makefile_am import MakefileAmSuite
from configure_ac import ConfigureACSuite
from output import AutomakeOutputSuite
from iface import InterfaceSuite

import unittest

class AutomakeSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)

        self.addTest(MakefileUtilsSuite())
        self.addTest(MakefileAmSuite())
        self.addTest(ConfigureACSuite())
        self.addTest(AutomakeOutputSuite())
        self.addTest(InterfaceSuite())
        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(AutomakeSuite())
    pass
