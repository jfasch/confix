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

from libconfix.core.filesys.file import File
from libconfix.core.coordinator import BuildCoordinator
from libconfix.plugins.c.setup import CSetupFactory
from libconfix.testutils import dirhier

import unittest

class HeaderInstallSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(HeaderInstallTest('test'))
        pass
    pass

class HeaderInstallTest(unittest.TestCase):
    def test(self):
        fs = dirhier.packageroot()
        file_h = fs.rootdirectory().add(name='file.h',
                                        entry=File())
        file_h.set_property(name='INSTALLPATH_CINCLUDE', value=['xxx'])
        coordinator = BuildCoordinator(root=fs.rootdirectory(),
                                       setups=[CSetupFactory(short_libnames=False,
                                                             use_libtool=False)])
        coordinator.enlarge()
        coordinator.output()

        self.failUnless(coordinator.rootbuilder().makefile_am().public_header_dir('file.h') == 'xxx')
        pass
        

if __name__ == '__main__':
    unittest.TextTestRunner().run(HeaderInstallSuite())
    pass
