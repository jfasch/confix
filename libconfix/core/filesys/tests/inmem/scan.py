# Copyright (C) 2007 Joerg Faschingbauer

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

from libconfix.core.filesys import scan
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.testutils.persistent import PersistentTestCase

import unittest

class ScanSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(NewFileTest('test'))
        pass
    pass

class NewFileTest(PersistentTestCase):
    def test(self):
        # use a filesystem instance to conveniently create the initial
        # directory.
        fs_orig = FileSystem(self.rootpath())
        fs_orig.rootdirectory().add(
            name='file1',
            entry=File())
        fs_orig.sync()
        
        # we have synced the fs_orig, so a scan should see file1
        fs_dup = scan.scan_filesystem(self.rootpath())
        self.failUnless(fs_dup.rootdirectory().get('file1'))

        # now add a file to the directory, via fs_orig
        fs_orig.rootdirectory().add(
            name='file2',
            entry=File())
        fs_orig.sync()

        # rescan the fs_dup's rootdirectory. the file must be seen.
        scan.rescan_dir(fs_dup.rootdirectory())
        self.failUnless(fs_dup.rootdirectory().get('file2'))
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(ScanSuite())
    pass
