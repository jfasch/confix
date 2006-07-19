#!/usr/bin/env python

import unittest

import libconfix.buildable_h

class NamespaceTest(unittest.TestCase):

    def test(self): self.runTest()

    def runTest(self):

        """simple namespace recognition"""

        c = libconfix.buildable_h.BuildableHeaderCreator()
        b = c.create_from_file(dir='data/buildables/ok',
                               filename='namespace.h')
        b.scan(None)
        b.validate()

        self.assert_(b.install_path() == 'X',
                     'install path of file data/buildables/namespace.h must be "X"')

        b = c.create_from_file(dir='data/buildables/nok',
                               filename='namespace.h')
        self.assertRaises(libconfix.error.Error, b.scan, None)

if __name__ == '__main__':
    unittest.main()
