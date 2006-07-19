# $Id: requires.py,v 1.4 2006/06/23 08:14:35 jfasch Exp $

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

from libconfix.plugins.c.c import CBuilder
from libconfix.plugins.c.dependency import Require_CInclude
from libconfix.core.filesys.file import File
from libconfix.core.require import Require

import unittest

class RequireTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(ScanTest())
        self.addTest(IfaceTest())
        pass

class ScanTest(unittest.TestCase):
    def runTest(self): self.test()
    def test(self):
        file = File(lines=['#include <inc1>',
                           '#include "inc2"',
                           '#   include <inc3>',
                           '#   include <inc4>   ',
                           '   #include <inc5>',
                           ])
        builder = CBuilder(file=file, parentbuilder=None, coordinator=None)
        self.assertEqual(len(builder.requires()), 5)
        inc1 = None
        inc2 = None
        inc3 = None
        inc4 = None
        inc5 = None
        for r in builder.requires():
            self.assert_(isinstance(r, Require_CInclude))
            if r.filename() == 'inc1':
                inc1 = r
                continue
            if r.filename() == 'inc2':
                inc2 = r
                continue
            if r.filename() == 'inc3':
                inc3 = r
                continue
            if r.filename() == 'inc4':
                inc4 = r
                continue
            if r.filename() == 'inc5':
                inc5 = r
                continue
            pass
        self.assertNotEqual(inc1, None)
        self.assertNotEqual(inc2, None)
        self.assertNotEqual(inc3, None)
        self.assertNotEqual(inc4, None)
        self.assertNotEqual(inc5, None)
        self.assertEqual(inc1.urgency(), Require.URGENCY_IGNORE)
        self.assertEqual(inc2.urgency(), Require.URGENCY_IGNORE)
        self.assertEqual(inc3.urgency(), Require.URGENCY_IGNORE)
        self.assertEqual(inc4.urgency(), Require.URGENCY_IGNORE)
        self.assertEqual(inc5.urgency(), Require.URGENCY_IGNORE)

        pass
    pass

class IfaceTest(unittest.TestCase):
    def runTest(self): self.test()
    def test(self):
        file = File(lines=[
            "// CONFIX:REQUIRE_H(filename='inc1')",
            "// CONFIX:REQUIRE_H(filename='inc2', urgency=Require.URGENCY_IGNORE)",
            "// CONFIX:REQUIRE_H(filename='inc3', urgency=Require.URGENCY_WARN)",
            "// CONFIX:REQUIRE_H(filename='inc4', urgency=Require.URGENCY_ERROR)",
            ])
        builder = CBuilder(file=file, parentbuilder=None, coordinator=None)
        self.assertEqual(len(builder.requires()), 4)
        inc1 = None
        inc2 = None
        inc3 = None
        inc4 = None
        for r in builder.requires():
            self.assert_(isinstance(r, Require_CInclude))
            if r.filename() == 'inc1':
                inc1 = r
                continue
            if r.filename() == 'inc2':
                inc2 = r
                continue
            if r.filename() == 'inc3':
                inc3 = r
                continue
            if r.filename() == 'inc4':
                inc4 = r
                continue
            pass
        self.assertNotEqual(inc1, None)
        self.assertNotEqual(inc2, None)
        self.assertNotEqual(inc3, None)
        self.assertNotEqual(inc4, None)
        self.assertEqual(inc1.urgency(), Require.URGENCY_IGNORE)
        self.assertEqual(inc2.urgency(), Require.URGENCY_IGNORE)
        self.assertEqual(inc3.urgency(), Require.URGENCY_WARN)
        self.assertEqual(inc4.urgency(), Require.URGENCY_ERROR)
        
    pass

if __name__ == '__main__':
    unittest.main()
