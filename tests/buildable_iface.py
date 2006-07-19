#!/usr/bin/env python

import unittest

import libconfix.buildable_cxx
import libconfix.error

class BuildableIfaceOkTest(unittest.TestCase):

    def test(self): self.runTest()

    def runTest(self):

        """Call all buildable-iface functions (no checks)"""

        b = libconfix.buildable_cxx.create('iface.cc', 'data/buildables/ok', 'iface.cc', None)
        b.scan()
        b.validate()

if __name__ == '__main__':
    unittest.main()
