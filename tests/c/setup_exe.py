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

from libconfix.core.filesys.file import File
from libconfix.core.local_package import LocalPackage
from libconfix.core.filebuilder import FileBuilder
from libconfix.plugins.c.setup import CSetup
from libconfix.plugins.c.h import HeaderBuilder
from libconfix.plugins.c.c import CBuilder
from libconfix.plugins.c.executable import ExecutableBuilder
from libconfix.plugins.c.library import LibraryBuilder
from libconfix.testutils import dirhier

import unittest

class ExecutableSetupTest(unittest.TestCase):

    def test(self):
        fs = dirhier.packageroot()
        fs.rootdirectory().add(name='file.h', entry=File(lines=[]))
        fs.rootdirectory().add(name='file.c', entry=File(lines=[]))
        main_c = File(lines=[])
        main_c.set_property(name='MAIN', value=True)
        fs.rootdirectory().add(name='main.c', entry=main_c)

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[CSetup(short_libnames=False,
                                              use_libtool=False)])
        package.enlarge(external_nodes=[])

        file_h_builder = None
        file_c_builder = None
        library_builder = None
        main_builder = None
        for b in package.rootbuilder().builders():
            if isinstance(b, FileBuilder):
                if b.file().name() == 'file.h' and isinstance(b, HeaderBuilder):
                    file_h_builder = b
                    pass
                elif b.file().name() == 'file.c' and isinstance(b, CBuilder):
                    file_c_builder = b
                    pass
                pass
            elif isinstance(b, LibraryBuilder):
                library_builder = b
                pass
            elif isinstance(b, ExecutableBuilder):
                if b.center().file().name() == 'main.c':
                    main_builder = b
                    pass
                pass
            pass
        self.assert_(isinstance(file_h_builder, HeaderBuilder))
        self.assert_(isinstance(file_c_builder, CBuilder))
        self.assert_(library_builder is None)
        self.assert_(isinstance(main_builder, ExecutableBuilder))

        pass

    pass
    
if __name__ == '__main__':
    unittest.main()
