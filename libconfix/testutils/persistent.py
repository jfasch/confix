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

import os, shutil

class PersistentTest:

    sequential_number = 0
    
    def __init__(self):
        pass

    def rootpath(self):
        return self.rootpath_

    def setUp(self):
        self.rootpath_ = ['', 'tmp',
                          'confix.'+str(os.getpid())+'.'+str(PersistentTest.sequential_number)+'.'+self.__class__.__name__]
        PersistentTest.sequential_number += 1
        pass

    def tearDown(self):
##         dir = os.sep.join(self.rootpath_)
##         if os.path.isdir(dir):
##             shutil.rmtree(dir)
##             pass
        pass
        
