# $Id: library.py,v 1.2 2006/07/12 08:42:21 jfasch Exp $

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

from libconfix.testutils import dirhier, find
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.utils import const
from libconfix.core.coordinator import BuildCoordinator
from libconfix.core.hierarchy import DirectorySetupFactory
from libconfix.plugins.c.setup import CSetupFactory
from libconfix.plugins.c.library import LibraryBuilder

import unittest

class LibrarySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(LibtoolLibrary('test_library_alone'))
        self.addTest(LibtoolLibrary('test_version'))
        self.addTest(ArchiveLibrary('test_library_alone'))
        pass
    pass

class LibraryBase(unittest.TestCase):
    def use_libtool(self): assert 0
    
    def setUp(self):
        self.fs_ = dirhier.packageroot()
        liblo = self.fs_.rootdirectory().add(name='lo', entry=Directory())
        liblo.add(name=const.MAKEFILE_PY,
                  entry=File(lines=["LIBTOOL_LIBRARY_VERSION((1,2,3))"]))
        liblo.add(name='lo.h',
                  entry=File(lines=['#ifndef LO_H',
                                    '#  define LO_H',
                                    '#endif',
                                    'void lo();']))
        liblo.add(name='lo.c',
                  entry=File(lines=['void lo() {}']))
        
        self.coordinator_ = BuildCoordinator(
            root=self.fs_.rootdirectory(),
            setups=[DirectorySetupFactory(),
                    CSetupFactory(short_libnames=False, # there is already a test for it, elsewhere
                                  use_libtool=self.use_libtool())])
        self.coordinator_.enlarge()
        self.coordinator_.output()

        self.lodir_builder_ = find.find_entrybuilder(self.coordinator_.rootbuilder(), ['lo'])
        self.lolib_builder_ = None
        for b in self.lodir_builder_.builders():
            if isinstance(b, LibraryBuilder):
                self.lolib_builder_ = b
                pass
            pass

        assert self.lolib_builder_ is not None

        pass
        
    def tearDown(self):
        self.fs_ = None
        self.coordinator_ = None
        pass
        
    def test_library_alone(self):
        mf_am = self.lodir_builder_.makefile_am()
        self.failIfEqual(mf_am, None)

        # we ought to be building a library here
        self.failUnlessEqual(self.lolib_builder_.basename(), 'blah_lo')
        self.failUnlessEqual(self.lolib_builder_.libname(), self.libname())
        self.failUnless(self.lolib_builder_.libname() in mf_am.dir_primary(dir='lib', primary=self.primary()))

        # lo.{h,c} are the sources

        sources = self.lodir_builder_.makefile_am().compound_sources(self.amlibname())
        self.failIf(sources is None)
        self.failUnless('lo.h' in sources)
        self.failUnless('lo.c' in sources)
        
        pass
    
    pass

class LibtoolLibrary(LibraryBase):
    def use_libtool(self): return True
    def libname(self): return 'libblah_lo.la'
    def amlibname(self): return 'libblah_lo_la'
    def primary(self): return 'LTLIBRARIES'

    def test_version(self):
        flags = self.lodir_builder_.makefile_am().compound_ldflags(self.amlibname())
        self.failIf(flags is None)
        self.failUnless('-version-info 1:2:3' in flags)
        pass
    pass

class ArchiveLibrary(LibraryBase):
    def use_libtool(self): return False
    def libname(self): return 'libblah_lo.a'
    def amlibname(self): return 'libblah_lo_a'
    def primary(self): return 'LIBRARIES'
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(LibrarySuite())
    pass
