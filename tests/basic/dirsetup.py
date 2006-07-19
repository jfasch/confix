# $Id: dirsetup.py,v 1.5 2006/06/23 08:14:35 jfasch Exp $

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
from libconfix.core.filebuilder import FileBuilder
from libconfix.core.hierarchy import DirectorySetupFactory, DirectoryBuilder

from libconfix.testutils import dirhier
from libconfix.testutils import find

import unittest
import types

class BasicDirectorySetup(unittest.TestCase):

    def test(self):
        fs = dirhier.packageroot()
        subdir = dirhier.subdir(parent=fs.rootdirectory(), name='a')
        subsubdir = dirhier.subdir(parent=subdir, name='a')
        
        coordinator = BuildCoordinator(
            root=fs.rootdirectory(),
            setups=[DirectorySetupFactory()])
        coordinator.enlarge()

        self.assertEqual(coordinator.rootbuilder().directory().find(['a']), subdir)
        self.assertEqual(coordinator.rootbuilder().directory().find(['a', 'a']), subsubdir)
        
        subdir_builder = find.find_entrybuilder(coordinator.rootbuilder(), ['a'])
        subsubdir_builder = find.find_entrybuilder(coordinator.rootbuilder(), ['a','a'])

        self.assertEqual(subdir_builder.directory(), subdir)
        self.assertEqual(subsubdir_builder.directory(), subsubdir)

        pass

    pass

if __name__ == '__main__':
    unittest.main()
    pass
