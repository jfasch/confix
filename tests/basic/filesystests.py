# $Id: filesystests.py,v 1.5 2006/06/27 15:08:59 jfasch Exp $

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

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.directory import Directory, DirectoryState
from libconfix.core.filesys.file import File, FileState
from libconfix.core.filesys.scan import scan_filesystem
from libconfix.core.utils.error import Error

import unittest, os, stat, shutil, sys

class FileSystemTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(Basics('test'))
        self.addTest(Sync('test_mem2sync'))
        self.addTest(Sync('test_dirty2sync'))
        self.addTest(Sync('test_filechange'))
        self.addTest(Sync('test_file_clear_on_sync_false'))
        self.addTest(Sync('test_file_clear_on_sync_true'))
        self.addTest(Sync('test_file_truncate_persistent'))
        self.addTest(Sync_RootMoreThanOneDirectoryDeep('test'))
        pass
    pass

class Basics(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=['a', 'b'])
        subdir = Directory()
        subdir.add(name='file', entry=File())
        fs.rootdirectory().add(name='subdir', entry=subdir)

        file = fs.rootdirectory().find(['subdir', 'file'])
        self.failIfEqual(file, None)
        self.failUnless(isinstance(file, File))

        self.assertEqual(subdir.abspath(), ['a', 'b', 'subdir'])
        self.assertEqual(subdir.relpath(), ['subdir'])

        self.assertRaises(Directory.AlreadyMounted, fs.rootdirectory().add, name='subdir', entry=File())

        pass

    pass

class Sync(unittest.TestCase):
    def setUp(self):
        self.rootpath_ = ['', 'tmp', 'confix.synctest.'+str(os.getpid())] 
        pass
    def tearDown(self):
        dir = os.sep.join(self.rootpath_)
        if os.path.isdir(dir):
            shutil.rmtree(dir)
            pass
        pass
        
    def test_mem2sync(self):
        fs = FileSystem(path=self.rootpath_)
        subdir = Directory(mode=0700)
        fs.rootdirectory().add(name='subdir', entry=subdir)
        file = File(mode=0755)
        subdir.add(name='file', entry=file)

        self.failUnlessEqual(fs.rootdirectory().state(), DirectoryState.INMEMORY)
        self.failUnlessEqual(subdir.state(), DirectoryState.INMEMORY)
        self.failUnlessEqual(file.state(), FileState.NEW)
        
        fs.sync()

        self.failUnlessEqual(fs.rootdirectory().state(), DirectoryState.SYNC)
        self.failUnlessEqual(subdir.state(), DirectoryState.SYNC)
        self.failUnlessEqual(file.state(), FileState.SYNC_INMEM)

        self.failUnless(os.path.isdir(os.sep.join(self.rootpath_)))
        self.failUnless(os.path.isdir(os.sep.join(self.rootpath_+['subdir'])))
        self.failUnless(os.path.isfile(os.sep.join(self.rootpath_+['subdir', 'file'])))

        self.failUnlessEqual(stat.S_IMODE(os.stat(os.sep.join(self.rootpath_+['subdir'])).st_mode), 0700)
        self.failUnlessEqual(stat.S_IMODE(os.stat(os.sep.join(self.rootpath_+['subdir', 'file'])).st_mode), 0755)
        pass

    def test_dirty2sync(self):
        fs = FileSystem(path=self.rootpath_)
        subdir = Directory(mode=0700)
        fs.rootdirectory().add(name='subdir', entry=subdir)
        file = File(mode=0755)
        subdir.add(name='file', entry=file)

        fs.sync()

        newfile = File()
        subdir.add(name='newfile', entry=newfile)
        self.failUnlessEqual(newfile.state(), FileState.NEW)

        fs.sync()

        self.failUnlessEqual(newfile.state(), FileState.SYNC_INMEM)
        self.failUnless(os.path.isfile(os.sep.join(self.rootpath_+['subdir', 'newfile'])))

        pass

    def test_filechange(self):
        # build up filesystem with our test file and sync it.
        fs = FileSystem(path=self.rootpath_)
        file = File(lines=['line 0'])
        fs.rootdirectory().add(name='file', entry=file)
        file.add_line('line 1')
        file.add_lines(['line 2', 'line 3'])
        fs.sync()

        # re-read our file and see if everything is there
        fs = scan_filesystem(path=self.rootpath_)
        file = fs.rootdirectory().find(['file'])
        lines = file.lines()
        self.failUnlessEqual(lines[0], 'line 0')
        self.failUnlessEqual(lines[1], 'line 1')
        self.failUnlessEqual(lines[2], 'line 2')
        self.failUnlessEqual(lines[3], 'line 3')
        file.add_line('line 4')
        fs.sync()

        # append to our file without explicitly reading it.
        fs = scan_filesystem(path=self.rootpath_)
        file = fs.rootdirectory().find(['file'])
        file.add_line('line 5')
        fs.sync()

        # see if there's still everything there.
        fs = scan_filesystem(path=self.rootpath_)
        file = fs.rootdirectory().find(['file'])
        lines = file.lines()
        self.failUnlessEqual(lines[0], 'line 0')
        self.failUnlessEqual(lines[1], 'line 1')
        self.failUnlessEqual(lines[2], 'line 2')
        self.failUnlessEqual(lines[3], 'line 3')
        self.failUnlessEqual(lines[4], 'line 4')
        self.failUnlessEqual(lines[5], 'line 5')
        pass

    def test_file_clear_on_sync_false(self):
        fs = FileSystem(path=self.rootpath_)
        file = File(lines=['line'])
        fs.rootdirectory().add(name='file', entry=file)
        fs.sync()
        self.failIf(file.lines_ is None)
        pass
        
    def test_file_clear_on_sync_true(self):
        fs = FileSystem(path=self.rootpath_, flags=set([FileSystem.CLEAR_ON_SYNC]))
        file = File(lines=['line'])
        fs.rootdirectory().add(name='file', entry=file)
        fs.sync()
        self.failUnless(file.lines_ is None)
        pass

    def test_file_truncate_persistent(self):
        fs = FileSystem(path=self.rootpath_)
        file = File(lines=['line'])
        fs.rootdirectory().add(name='file', entry=file)
        fs.sync()

        fs = scan_filesystem(path=self.rootpath_)
        file = fs.rootdirectory().find(['file'])
        file.truncate()
        fs.sync()

        fs = scan_filesystem(path=self.rootpath_)
        file = fs.rootdirectory().find(['file'])
        self.failUnless(file.lines() == [])
        pass

    pass

class Sync_RootMoreThanOneDirectoryDeep(unittest.TestCase):

    # the above tests only test syncing an in-memory filesystem whose
    # root is only one directory apart from a pysical directory. here
    # we test whether it work with two directory entries in the air as
    # well.
    
    def test(self):
        path = ['', 'tmp', 'confix.synctest.'+str(os.getpid()), str(self.__class__)]
        fs = FileSystem(path=path)
        fs.sync()
        self.failUnless(os.path.isdir(os.sep.join(path)))
        pass
    pass
        

if __name__ == '__main__':
    unittest.main()
    pass
