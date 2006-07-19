# $Id: ltlibrary.py,v 1.2 2006/07/13 20:27:24 jfasch Exp $

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

from libconfix.core.coordinator import BuildCoordinator
from libconfix.core.hierarchy import DirectorySetupFactory
from libconfix.testutils import dirhier, find
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.utils import const

from libconfix.plugins.c.setup import CSetupFactory

import unittest

class LibtoolLibrarySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(LibtoolLibrary_LIBADD('test'))
        pass
    pass

class LibtoolLibrary_LIBADD(unittest.TestCase):

    # _LIBADD contains only the direct dependencies.

    # test package is

    # hi1->lo
    # hi2->lo
    # hiest->hi1
    # hiest->hi2

    # hiest _LIBADD must only contain hi1 and hi2, but not lo
    
        
    def test(self):
        fs = dirhier.packageroot()
        dirlo = fs.rootdirectory().add(name='lo', entry=Directory())
        dirlo.add(name=const.MAKEFILE_PY, entry=File())
        dirlo.add(name='lo.h', entry=File())
        dirlo.add(name='lo.c', entry=File())
        
        dirhi1 = fs.rootdirectory().add(name='hi1', entry=Directory())
        dirhi1.add(name=const.MAKEFILE_PY, entry=File())
        dirhi1.add(name='hi1.h', entry=File(lines=['#include <lo.h>']))
        dirhi1.add(name='hi1.c', entry=File())
        
        dirhi2 = fs.rootdirectory().add(name='hi2', entry=Directory())
        dirhi2.add(name=const.MAKEFILE_PY, entry=File())
        dirhi2.add(name='hi2.h', entry=File(lines=['#include <lo.h>']))
        dirhi2.add(name='hi2.c', entry=File())
        
        dirhiest = fs.rootdirectory().add(name='hiest', entry=Directory())
        dirhiest.add(name=const.MAKEFILE_PY, entry=File())
        dirhiest.add(name='hiest.h', entry=File(lines=['#include <hi1.h>', '#include <hi2.h>']))
        dirhiest.add(name='hiest.c', entry=File())
        
        coordinator = BuildCoordinator(
            root=fs.rootdirectory(),
            setups=[DirectorySetupFactory(),
                    CSetupFactory(short_libnames=False, # don't care
                                  use_libtool=True)])
        coordinator.enlarge()
        coordinator.output()

        hiestdir_builder = find.find_entrybuilder(coordinator.rootbuilder(), ['hiest'])
        self.failIf(hiestdir_builder is None)

        self.failUnlessEqual(len(hiestdir_builder.makefile_am().compound_libadd('libblah_hiest_la')), 2)
        
        self.failUnless('$(top_builddir)/hi1/libblah_hi1.la' in \
                        hiestdir_builder.makefile_am().compound_libadd('libblah_hiest_la'))
        self.failUnless('$(top_builddir)/hi2/libblah_hi2.la' in \
                        hiestdir_builder.makefile_am().compound_libadd('libblah_hiest_la'))
        pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(LibtoolLibrarySuite())
    pass
