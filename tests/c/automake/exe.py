# $Id: exe.py,v 1.3 2006/07/13 20:36:18 jfasch Exp $

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
from libconfix.plugins.c.executable import ExecutableBuilder
from libconfix.plugins.c.library import LibraryBuilder

import unittest

class ExecutableSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(LibtoolExecutable('common_test'))
        self.addTest(StandardExecutable('common_test'))
        self.addTest(LibtoolExecutable('test'))
        self.addTest(StandardExecutable('test'))
        pass
    pass

class ExecutableBase(unittest.TestCase):
    def use_libtool(self): assert 0, 'abstract'
    def setUp(self):
        self.fs_ = dirhier.packageroot()
        liblo = self.fs_.rootdirectory().add(name='lo', entry=Directory())
        liblo.add(name=const.MAKEFILE_PY, entry=File(lines=[]))
        liblo.add(name='lo.h',
                  entry=File(lines=['#ifndef LO_H',
                                    '#define LO_H',
                                    'void lo();',
                                    '#endif',
                                    ]))
        liblo.add(name='lo.c',
                  entry=File(lines=['void lo() {}']))
        
        libhi = self.fs_.rootdirectory().add(name='hi', entry=Directory())
        libhi.add(name=const.MAKEFILE_PY, entry=File(lines={}))
        libhi.add(name='hi.h',
                   entry=File(lines=['#ifndef HI_H',
                                     '#  define HI_H',
                                     '#endif',
                                     'void hi();']))
        libhi.add(name='hi.c',
                   entry=File(lines=['#include <hi.h>',
                                     '#include <lo.h>',
                                     'void hi() { lo(); }']))
        
        exe = self.fs_.rootdirectory().add(name='exe', entry=Directory())
        exe.add(name=const.MAKEFILE_PY, entry=File(lines=[]))
        exe.add(name='main.c',
                entry=File(lines=['#include <hi.h>',
                                  'int main(void) {',
                                  '    hi();',
                                  '    return 0;',
                                  '}']))
        exe.add(name='something.c', entry=File())
        
        self.coordinator_ = BuildCoordinator(root=self.fs_.rootdirectory(),
                                             setups=[DirectorySetupFactory(),
                                                     CSetupFactory(short_libnames=False, use_libtool=self.use_libtool())])
        self.coordinator_.enlarge()
        self.coordinator_.output()

        self.lodir_builder_ = find.find_entrybuilder(self.coordinator_.rootbuilder(), ['lo'])
        self.hidir_builder_ = find.find_entrybuilder(self.coordinator_.rootbuilder(), ['hi'])
        self.exedir_builder_ = find.find_entrybuilder(self.coordinator_.rootbuilder(), ['exe'])
        assert self.lodir_builder_
        assert self.hidir_builder_
        assert self.exedir_builder_

        self.lolib_builder_ = None
        self.hilib_builder_ = None
        self.exe_builder_ = None

        for b in self.lodir_builder_.builders():
            if isinstance(b, LibraryBuilder):
                self.lolib_builder_ = b
                pass
            pass
        for b in self.hidir_builder_.builders():
            if isinstance(b, LibraryBuilder):
                self.hilib_builder_ = b
                pass
            pass
        for b in self.exedir_builder_.builders():
            if isinstance(b, ExecutableBuilder):
                self.exe_builder_ = b
                pass
            pass
        pass

    def tearDown(self):
        self.fs_ = None
        self.coordinator_ = None
        pass

    def common_test(self):
        self.failUnless('blah_exe_main' in self.exedir_builder_.makefile_am().bin_programs())
        self.failUnless('main.c' in self.exedir_builder_.makefile_am().compound_sources('blah_exe_main'))
        self.failUnless('something.c' in self.exedir_builder_.makefile_am().compound_sources('blah_exe_main'))
        pass
    pass

class LibtoolExecutable(ExecutableBase):
    def use_libtool(self): return True

    # a libtool executable must have only its direct dependencies on
    # the link line.

    def test(self):
        self.failUnlessEqual(len(self.exedir_builder_.makefile_am().compound_ldadd('blah_exe_main')), 1)
        self.failUnlessEqual(self.exedir_builder_.makefile_am().compound_ldadd('blah_exe_main')[0],
                             '$(top_builddir)/hi/libblah_hi.la')
        pass
    pass

class StandardExecutable(ExecutableBase):
    def use_libtool(self): return False

    # a standard (non-libtool) executable must have all its
    # dependencies, in reverse-topological order.

    def test(self):
        self.failUnlessEqual(self.exedir_builder_.makefile_am().compound_ldadd('blah_exe_main'),
                             ['$(top_builddir)/hi/libblah_hi.a', '$(top_builddir)/lo/libblah_lo.a'])
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(ExecutableSuite())
    pass
