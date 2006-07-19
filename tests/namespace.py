#!/usr/bin/env python

import unittest

import libconfix.buildable_h

class NamespaceTest(unittest.TestCase):

    def test(self): self.runTest()

    def runTest(self):

        """simple namespace recognition"""

        b = libconfix.buildable_h.create('namespace.h', 'data/buildables/ok', 'namespace.h', None)
        b.scan()
        b.validate()

        self.assert_(b.get_install_path() == 'X',
                     'install path of file data/buildables/namespace.h must be "X"')

        b = libconfix.buildable_h.create('namespace.h', 'data/buildables/nok', 'namespace.h', None)
        self.assertRaises(libconfix.error.Error, b.scan)

if __name__ == '__main__':
    unittest.main()
