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

from source import source_tree

from libconfix.core.machinery.local_package import LocalPackage
from libconfix.plugins.c.setup import DefaultCSetup

import unittest

class ReadonlyPrefixesIncludePathInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(ReadonlyPrefixesIncludePathInMemoryTest('test'))
        pass
    pass

class ReadonlyPrefixesIncludePathInMemoryTest(unittest.TestCase):
    def test(self):
        source = source_tree(testname=self.__class__.__name__)
        lo_dir = source.get('lo')
        hi_dir = source.get('hi')

        lo_pkg = LocalPackage(rootdirectory=lo_dir, setups=[DefaultCSetup(short_libnames=False, use_libtool=False)])
        lo_pkg.boil(external_nodes=[])
        lo_pkg_inst = lo_pkg.install()

        hi_pkg = LocalPackage(rootdirectory=hi_dir, setups=[DefaultCSetup(short_libnames=False, use_libtool=False)])
        hi_pkg.boil(external_nodes=lo_pkg_inst.nodes())
        hi_pkg.output()

        makefile_am = hi_pkg.rootbuilder().makefile_am()
        self.failUnless('$(readonly_prefixes_incpath)' in makefile_am.includepath())
        pass
    pass        

if __name__ == '__main__':
    unittest.TextTestRunner().run(ReadonlyPrefixesIncludePathInMemorySuite())
    pass
        