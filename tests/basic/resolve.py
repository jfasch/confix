# $Id: resolve.py,v 1.8 2006/07/07 15:29:19 jfasch Exp $

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
from libconfix.testutils import find
from libconfix.testutils.ifacetestbuilder import FileInterfaceTestSetupFactory

from libconfix.core.edgefinder import EdgeFinder
from libconfix.core.require_symbol import Require_Symbol
from libconfix.core.filesys.file import File
from libconfix.core.coordinator import BuildCoordinator
from libconfix.core.hierarchy import DirectorySetupFactory
from libconfix.core.digraph.cycle import CycleError
import unittest

class ResolveTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(BasicResolveTest())
        self.addTest(NotResolvedTest())
        self.addTest(CycleTest())
        pass

class BasicResolveTest(unittest.TestCase):
    def runTest(self): self.test()
    def test(self):
        fs = dirhier.packageroot()

        lodir = dirhier.subdir(fs.rootdirectory(), 'lo')
        lofile = lodir.add(name='lo.iface',
                           entry=File(lines=['PROVIDE_SYMBOL(symbol="lo")']))
        
        hidir = dirhier.subdir(fs.rootdirectory(), 'hi')
        hifile = hidir.add(name='hi.iface',
                           entry=File(lines=['REQUIRE_SYMBOL(symbol="lo", urgency=URGENCY_ERROR)']))

        coordinator = BuildCoordinator(root=fs.rootdirectory(),
                                       setups=[DirectorySetupFactory(),
                                               FileInterfaceTestSetupFactory()])
        coordinator.enlarge()

        lodirbuilder = find.find_entrybuilder(coordinator.rootbuilder(), ['lo'])
        hidirbuilder = find.find_entrybuilder(coordinator.rootbuilder(), ['hi'])

        self.assertEqual(len(coordinator.digraph().nodes()), 3 \
                         # plus 1 for confix-admin which is a full-fledged node
                         +1)
        rootnode = None
        lonode = None
        hinode = None
        for n in coordinator.digraph().nodes():
            if n.responsible_builder() is coordinator.rootbuilder():
                rootnode = n
                continue
            if n.responsible_builder() is lodirbuilder:
                lonode = n
                continue
            if n.responsible_builder() is hidirbuilder:
                hinode = n
                continue
            pass

        self.assertEqual(len(coordinator.digraph().successors(hinode)), 1)
        self.assertEqual(len(coordinator.digraph().successors(lonode)), 0)
        self.assert_(lonode in coordinator.digraph().successors(hinode))
            
        pass
    
    pass

class NotResolvedTest(unittest.TestCase):
    def runTest(self): self.test()
    def test(self):
        fs = dirhier.packageroot()
        file = fs.rootdirectory().add(name='x.iface',
                                      entry=File(lines=['REQUIRE_SYMBOL(symbol="unknown_symbol", urgency=URGENCY_ERROR)']))

        coordinator = BuildCoordinator(root=fs.rootdirectory(),
                                       setups=[FileInterfaceTestSetupFactory()])

        try:
            coordinator.enlarge()
            pass
        except EdgeFinder.SuccessorNotFound, e:
            self.assert_(e.node().responsible_builder() is coordinator.rootbuilder())
            self.assert_(isinstance(e.errors()[0], EdgeFinder.RequireNotResolved))
            self.assert_(isinstance(e.errors()[0].require(), Require_Symbol))
            self.assert_(e.errors()[0].require().symbol() == 'unknown_symbol')
            return

        self.fail()
        pass
    
    pass

class CycleTest(unittest.TestCase):
    def runTest(self): self.test()
    def test(self):
        fs = dirhier.packageroot()

        dirA = dirhier.subdir(fs.rootdirectory(), 'A')
        fileA = dirA.add(name='A.iface',
                         entry=File(lines=['PROVIDE_SYMBOL(symbol="A")',
                                           'REQUIRE_SYMBOL(symbol="B")']))
        
        dirB = dirhier.subdir(fs.rootdirectory(), 'B')
        fileB = dirB.add(name='B.iface',
                         entry=File(lines=['PROVIDE_SYMBOL(symbol="B")',
                                           'REQUIRE_SYMBOL(symbol="A")']))

        coordinator = BuildCoordinator(root=fs.rootdirectory(),
                                       setups=[DirectorySetupFactory(),
                                               FileInterfaceTestSetupFactory()])
        try:
            coordinator.enlarge()
        except CycleError:
            return
        self.fail()
        pass
    pass

if __name__ == '__main__':
    unittest.main()
    pass

