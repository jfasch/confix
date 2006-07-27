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

from libconfix.testutils import dirhier
from libconfix.core.filesys.file import File
from libconfix.core.local_package import LocalPackage
from libconfix.core.hierarchy import DirectorySetupFactory
from libconfix.plugins.c.setup import CSetupFactory

import unittest

class CSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(CTest('test'))
        pass
    pass

class CTest(unittest.TestCase):
    def test(self):
        fs = dirhier.packageroot()
        fs.rootdirectory().add(name='file.h',
                               entry=File(lines=['#ifndef FILE_H',
                                                 '#define FILE_H',
                                                 'extern int i;'
                                                 '#endif',
                                                 ]))
        fs.rootdirectory().add(name='file.c',
                               entry=File(lines=['#include "file.h"',
                                                 'int i;',
                                                 ]))

        package = LocalPackage(
            root=fs.rootdirectory(),
            setups=[DirectorySetupFactory(),
                    CSetupFactory(short_libnames=False,
                                  use_libtool=False)])
        package.enlarge(external_nodes=[])
        package.output()

        conf_ac = fs.rootdirectory().find(['configure.ac'])
        self.failIf(conf_ac is None)
        found_AC_PROG_CC = False
        for l in conf_ac.lines():
            if l == 'AC_PROG_CC':
                found_AC_PROG_CC = True
                continue
            pass

        self.failUnless(found_AC_PROG_CC)
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(CSuite())
    pass
