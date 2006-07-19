# $Id: property.py,v 1.2 2006/06/23 08:14:35 jfasch Exp $

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

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File

import unittest

class Property(unittest.TestCase):
    def test(self):
        dir = Directory()
        file = File()

        dir.set_property(name='a', value='b')
        file.set_property(name='c', value='d')

        self.assertEqual(dir.get_property('a'), 'b')
        self.assertEqual(file.get_property('c'), 'd')

        dir.del_property(name='a')
        file.del_property(name='c')

        self.assertEqual(dir.get_property('a'), None)
        self.assertEqual(file.get_property('c'), None)

        pass
    pass

if __name__ == '__main__':
    unittest.main()
    pass
