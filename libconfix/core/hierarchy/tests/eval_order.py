# Copyright (C) 2008 Joerg Faschingbauer

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

from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.hierarchy.confix2_dir_contributor import Confix2_dir_Contributor
from libconfix.core.hierarchy.confix2_dir import Confix2_dir
from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.utils import const

import unittest

class IfaceEvaluationOrderSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(IfaceEvaluationOrderTest('test'))
        pass
    pass

class TestIface(Confix2_dir_Contributor):
    class TEST_IFACE(InterfaceProxy):
        def __init__(self, object):
            InterfaceProxy.__init__(self, object)
            self.add_global('TEST_IFACE', getattr(self, 'TEST_IFACE'))
            self.__object = object
            self.__called = False
            pass
        def TEST_IFACE(self):
            self.__object.set_called()
            pass
        pass
    def locally_unique_id(self):
        return self.__class__.__name__
    def get_iface_proxies(self):
        return [self.TEST_IFACE(self)]
    def set_called(self):
        self.__called = True
        pass
    def is_called(self):
        return self.__called
    pass

# we have a bloody order dependency in the interface evaluation
# code. if one Confix2.dir contributor comes after the Confix2.dir
# file builder itself, then things go wrong. went wrong, better to
# say: this test made it right.
class IfaceEvaluationOrderTest(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=["don't", 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("'+self.__class__.__name__+'")',
                              'PACKAGE_VERSION("1.2.3")']))
        confix2_dir = fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['TEST_IFACE()']))

        test_iface = TestIface()
        
        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[])

        # add Confix2_dir, and then the iface for it.
        package.rootbuilder().add_builder(Confix2_dir(file=confix2_dir))
        package.rootbuilder().add_builder(test_iface)
        
        package.boil(external_nodes=[])
        self.failUnless(test_iface.is_called())
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(IfaceEvaluationOrderSuite())
    pass


