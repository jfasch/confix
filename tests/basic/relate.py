# Copyright (C) 2002-2006 Salomon Automation
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

from libconfix.testutils import dirhier
from libconfix.testutils import find
from libconfix.testutils.ifacetestbuilder import FileInterfaceTestSetup

from libconfix.core.filesys.file import File
from libconfix.core.local_package import LocalPackage
from libconfix.core.hierarchy.setup import DirectorySetup

import unittest

class RelateTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(RelateBasic('test'))
        self.addTest(InternalRequires('test'))
        pass
    pass

class RelateBasic(unittest.TestCase):

    """ See if we are calculating dependencies correctly. """
    
    def test(self):
        fs = dirhier.packageroot()

        lodir = dirhier.subdir(fs.rootdirectory(), 'lo')
        lofile = lodir.add(
            name='lo.iface',
            entry=File(lines=['PROVIDE_SYMBOL(symbol="lo")']))
        
        hidir = dirhier.subdir(fs.rootdirectory(), 'hi')
        hifile = hidir.add(
            name='hi.iface',
            entry=File(lines=['REQUIRE_SYMBOL(symbol="lo", urgency=URGENCY_ERROR)']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DirectorySetup(),
                                       FileInterfaceTestSetup()])
        package.enlarge(external_nodes=[])

        lodirbuilder = find.find_entrybuilder(package.rootbuilder(), ['lo'])
        hidirbuilder = find.find_entrybuilder(package.rootbuilder(), ['hi'])
        lofilebuilder = find.find_entrybuilder(package.rootbuilder(), ['lo', 'lo.iface'])
        hifilebuilder = find.find_entrybuilder(package.rootbuilder(), ['hi', 'hi.iface'])

        rootnode = find.find_managing_node_of_builder(package.digraph().nodes(), package.rootbuilder())
        lonode = find.find_managing_node_of_builder(package.digraph().nodes(), lodirbuilder)
        hinode = find.find_managing_node_of_builder(package.digraph().nodes(), hidirbuilder)

        self.failIf(lofilebuilder.successors() is None)
        self.failUnlessEqual(len(lofilebuilder.successors()), 0)
        self.failUnlessEqual(len(hifilebuilder.successors()), 1)
        self.failUnless(lonode in hifilebuilder.successors())
        self.failUnless(lofilebuilder.node() is lonode)
        self.failUnless(hifilebuilder.node() is hinode)
        self.failUnlessEqual(lofilebuilder.relate_calls(), 1)
        self.failUnlessEqual(hifilebuilder.relate_calls(), 1)
        
        pass
    pass

class InternalRequires(unittest.TestCase):

    """ Require objects of one node that are resolved by the same node
    must not molest the dependency calculation."""
    
    def test(self):
        fs = dirhier.packageroot()
        providing_file = fs.rootdirectory().add(
            name='providing_file.iface',
            entry=File(lines=['PROVIDE_SYMBOL(symbol="the_symbol_which_it_is_all_about")']))
        requiring_file = fs.rootdirectory().add(
            name='requiring_file.iface',
            entry=File(lines=['REQUIRE_SYMBOL(symbol="the_symbol_which_it_is_all_about",',
                              '               urgency=URGENCY_ERROR)']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DirectorySetup(),
                                       FileInterfaceTestSetup()])
        package.enlarge(external_nodes=[])

        rootnode = find.find_managing_node_of_builder(nodes=package.digraph().nodes(),
                                                      builder=package.rootbuilder())
        self.failUnlessEqual(len(rootnode.requires()), 0)
        pass
    pass

if __name__ == '__main__':
    unittest.main()
    pass

