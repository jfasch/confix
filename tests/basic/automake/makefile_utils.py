# $Id: FILE-HEADER,v 1.4 2006/02/06 21:07:44 jfasch Exp $

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

from libconfix.core.automake.rule import Rule

import unittest

class MakefileUtilsSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(RuleTest('test'))
        pass
    pass

class RuleTest(unittest.TestCase):
    def test(self):
        rule = Rule(targets=['target'],
                    prerequisites=['prereq1', 'prereq2'],
                    commands=['command1', 'command2'])
        lines = rule.lines()
        self.fail('makefileparser implementieren')
        pass
    pass


if __name__ == '__main__':
    unittest.TextTestRunner().run(MakefileUtilsSuite())
    pass
