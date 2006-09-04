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
from libconfix.core.filesys.file import File
from libconfix.core.local_package import LocalPackage
from libconfix.plugins.c.setup import CSetupFactory
from libconfix.plugins.c.library import LibraryBuilder
from libconfix.plugins.c.buildinfo import BuildInfo_CLibrary_NativeInstalled

import unittest

class InterPackageInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(InterPackageRelate('test'))
        pass
    pass

class InterPackageRelate(unittest.TestCase):
    def test(self):
        lofs = dirhier.packageroot(name='lo', version='1.2.3')
        lofs.rootdirectory().add(name='lo.h', entry=File())
        lofs.rootdirectory().add(name='lo.c', entry=File())
        local_lopkg = LocalPackage(root=lofs.rootdirectory(),
                                   setups=[CSetupFactory(short_libnames=False, use_libtool=False)])
        local_lopkg.enlarge(external_nodes=[])
        installed_lopkg = local_lopkg.install()

        hifs = dirhier.packageroot(name='hi', version='1.2.3')
        hifs.rootdirectory().add(name='hi.c',
                                 entry=File(lines=['#include <lo.h>']))
        local_hipkg = LocalPackage(root=hifs.rootdirectory(),
                                   setups=[CSetupFactory(short_libnames=False, use_libtool=False)])
        local_hipkg.enlarge(external_nodes=installed_lopkg.nodes())

        lo_h_builder = find.find_entrybuilder(root=local_lopkg.rootbuilder(), path=['lo.h'])
        lo_c_builder = find.find_entrybuilder(root=local_lopkg.rootbuilder(), path=['lo.c'])
        liblo_builder = None
        for b in local_lopkg.rootbuilder().builders():
            if isinstance(b, LibraryBuilder):
                liblo_builder = b
                break
            pass
        else:
            self.fail()
            pass

        hi_c_builder = find.find_entrybuilder(root=local_hipkg.rootbuilder(), path=['hi.c'])
        libhi_builder = None
        for b in local_hipkg.rootbuilder().builders():
            if isinstance(b, LibraryBuilder):
                libhi_builder = b
                break
            pass
        else:
            self.fail()
            pass

        # hi.c includes lo.h, so it must have a BuildInfo for
        # installed header files, but none for local header files.
        self.failUnless(hi_c_builder.buildinfo_includepath_native_installed() == 1)
        self.failUnless(hi_c_builder.buildinfo_includepath_native_local() == 0)
        self.failUnless(len(libhi_builder.buildinfo_direct_dependent_libs()) == 1)
        self.failUnless(len(libhi_builder.buildinfo_topo_dependent_libs()) == 1)
        self.failUnless(isinstance(libhi_builder.buildinfo_direct_dependent_libs()[0],
                                   BuildInfo_CLibrary_NativeInstalled))
        self.failUnless(isinstance(libhi_builder.buildinfo_topo_dependent_libs()[0],
                                   BuildInfo_CLibrary_NativeInstalled))
        self.failUnless(libhi_builder.buildinfo_topo_dependent_libs()[0] is \
                        libhi_builder.buildinfo_direct_dependent_libs()[0])                        
        self.failUnless(libhi_builder.buildinfo_direct_dependent_libs()[0].name() == 'lo')
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(InterPackageInMemorySuite())
    pass
        
